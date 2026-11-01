"""Build reproducible DE440 apparent-longitude models for the browser calculator.

Optional generation dependencies: skyfield==1.54, numpy (not needed by MkDocs).
Download the official de440.bsp separately; it is never committed. Example:
python tools/build_solar_term_model.py --kernel /tmp/de440.bsp --as-of 2026-11-01
The browser solves the longitude crossings, rather than looking up event times.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440.bsp'
DEGREE=14
SPAN_DAYS=8
KST=timezone(timedelta(hours=9))
TERMS=['춘분','청명','곡우','입하','소만','망종','하지','소서','대서','입추','처서','백로','추분','한로','상강','입동','소설','대설','동지','소한','대한','입춘','우수','경칩']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kernel',type=Path,required=True)
    p.add_argument('--start',type=int,default=1900)
    p.add_argument('--end',type=int,default=2100)
    p.add_argument('--as-of',required=True,help='UTC data preparation date, YYYY-MM-DD')
    p.add_argument('--output',type=Path,default=ROOT/'docs/assets/solar-terms/de440')
    a=p.parse_args()
    if not 1550<=a.start<=a.end<=2649: p.error('Complete DE440 years: 1550–2649')
    datetime.strptime(a.as_of,'%Y-%m-%d')
    import numpy as np
    import skyfield
    from skyfield.api import load,load_file
    from skyfield.nutationlib import iau2000b_radians
    from skyfield import almanac,almanac_east_asia
    ts=load.timescale(builtin=True)
    eph=load_file(str(a.kernel))
    if not all(getattr(s,'source',b'').startswith(b'DE-0440') for s in eph.spk.segments):
        raise ValueError('Expected the official DE440 kernel, not another ephemeris')
    earth,sun=eph['earth'],eph['sun']
    def longitude(seconds):
        # UTC datetimes provide Skyfield's explicit UTC -> TAI -> TT -> TDB conversion.
        dates=[datetime.fromtimestamp(float(s),timezone.utc) for s in np.asarray(seconds).ravel()]
        t=ts.from_datetimes(dates)
        t._nutation_angles_radians=iau2000b_radians(t)
        return earth.at(t).observe(sun).apparent().ecliptic_latlon('date')[1].degrees
    nodes=np.cos(np.pi*(np.arange(DEGREE+1)+.5)/(DEGREE+1))
    decades={}
    references={}
    worst=0.0
    for year in range(a.start,a.end+1):
        start=datetime(year,1,1,tzinfo=KST).astimezone(timezone.utc)
        end=datetime(year+1,1,1,tzinfo=KST).astimezone(timezone.utc)
        days=(end-start).days
        boundaries=set(np.arange(0,days,SPAN_DAYS,dtype=float)) | {float(days)}
        # UTC has jumps in its TT offset at known leap-second boundaries.
        # Fit each side independently instead of smoothing across that jump.
        for leap in ts.leap_dates:
            offset=((float(leap)-2440587.5)*86400-start.timestamp())/86400
            if 0<offset<days: boundaries.add(offset)
        boundaries=np.array(sorted(boundaries));starts=boundaries[:-1];ends=boundaries[1:]
        sample=(starts[:,None]+ends[:,None])/2+(ends-starts)[:,None]/2*nodes
        lon=longitude(start.timestamp()+sample.ravel()*86400).reshape(sample.shape)
        unwrapped=np.degrees(np.unwrap(np.radians(lon),axis=1))
        coeff=np.polynomial.chebyshev.chebfit(nodes,unwrapped.T,DEGREE).T
        coeff=np.round(coeff,12)
        probes=np.linspace(-1+1e-6,1-1e-6,19)
        probe_days=(starts[:,None]+ends[:,None])/2+(ends-starts)[:,None]/2*probes
        truth=longitude(start.timestamp()+probe_days.ravel()*86400).reshape(probe_days.shape)
        interpolated=np.array([np.polynomial.chebyshev.chebval(probes,c) for c in coeff])
        delta=(interpolated-truth+180)%360-180
        error=float(np.max(np.abs(delta))/0.94*86400)
        worst=max(worst,error)
        if error>.25:raise ValueError(f'{year}: interpolation error {error:.6f}s exceeds .25s')
        decades.setdefault(year//10*10,{})[str(year)]=[[float(first),float(last),*row] for first,last,row in zip(starts,ends,coeff.tolist())]
        if year in [1900,1920,2000,2026,2027,2028,2099,2100]:
            t,indices=almanac.find_discrete(ts.from_datetime(start),ts.from_datetime(end),almanac_east_asia.solar_terms(eph))
            if len(t)!=24:raise ValueError(f'{year}: expected 24 independent reference events')
            references[str(year)]=[[int(index),time.utc_iso(places=3)] for time,index in zip(t,indices)]
        if year%25==0 or year==a.end:print(f'DE440 model through {year}; worst probe error {worst:.6f}s',flush=True)
    a.output.mkdir(parents=True,exist_ok=True)
    for decade,years in decades.items():
        (a.output/f'{decade}.json').write_text(json.dumps({'schema':1,'years':years},ensure_ascii=False,separators=(',',':'))+'\n')
    metadata={'schema':1,'model':'JPL DE440','startYear':a.start,'endYear':a.end,'spanDays':SPAN_DAYS,'degree':DEGREE,'segmentLayout':'startDay,endDay,15 Chebyshev coefficients','timezone':'Asia/Seoul','offsetMinutes':540,'generatedOn':a.as_of,'skyfieldVersion':skyfield.__version__,'numpyVersion':np.__version__,'kernelUrl':SOURCE,'kernelSha256':hashlib.sha256(a.kernel.read_bytes()).hexdigest(),'frame':'geocentric apparent ecliptic longitude of date; IAU 2000B nutation','timeScale':'UTC inputs converted by Skyfield builtin timescale to TT/TDB; future leap seconds unknown','maxProbeErrorSeconds':round(worst,6),'referenceEventsUtc':references,'terms':TERMS,'skyfieldUrl':'https://rhodesmill.org/skyfield/almanac.html#solar-terms'}
    (a.output/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print(f'Wrote {a.end-a.start+1} years in {len(decades)} lazy-load decade files',flush=True)

if __name__=='__main__':main()
