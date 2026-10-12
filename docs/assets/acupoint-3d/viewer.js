/* 3D 경혈 지도: user-provided geometry and coordinates adapted to the archive. */
(async function () {
  try {
    const load = async path => { const r=await fetch(path,{credentials:'same-origin'}); if(!r.ok) throw new Error('자료를 불러오지 못했습니다.'); return r.json(); };
    const [data, MODEL] = await Promise.all([load('./points.json'),load('./model.json')]);
    const POINTS=data.points, MERIDIANS=data.meridians, PTD=data.positions, LINES=data.lines;
    const DAILY_CODES=["LU1", "LU2", "LU3", "LU4", "LU5", "LU6", "LU7", "LU8", "LU9", "LU10", "LU11", "LI1", "LI2", "LI3", "LI4", "LI5", "LI6", "LI7", "LI8", "LI9", "LI10", "LI11", "LI12", "LI13", "LI14", "LI15", "LI16", "LI17", "LI18", "LI19", "LI20", "ST1", "ST2", "ST3", "ST4", "ST5", "ST6", "ST7", "ST8", "ST9", "ST10", "ST11", "ST12", "ST13", "ST14", "ST15", "ST16", "ST17", "ST18", "ST19", "ST20", "ST21", "ST22", "ST23", "ST24", "ST25", "ST26", "ST27", "ST28", "ST29", "ST30", "ST31", "ST32", "ST33", "ST34", "ST35", "ST36", "ST37", "ST38", "ST39", "ST40", "ST41", "ST42", "ST43", "ST44", "ST45", "SP1", "SP2", "SP3", "SP4", "SP5", "SP6", "SP7", "SP8", "SP9", "SP10", "SP11", "SP12", "SP13", "SP14", "SP15", "SP16", "SP17", "SP18", "SP19", "SP20", "SP21", "HT1", "HT2", "HT3", "HT4", "HT5", "HT6", "HT7", "HT8", "HT9", "SI1", "SI2", "SI3", "SI4", "SI5", "SI6", "SI7", "SI8", "SI9", "SI10", "SI11", "SI12", "SI13", "SI14", "SI15", "SI16", "SI17", "SI18", "SI19", "BL1", "BL2", "BL3", "BL4", "BL5", "BL6", "BL7", "BL8", "BL9", "BL10", "BL11", "BL12", "BL13", "BL14", "BL15", "BL16", "BL17", "BL18", "BL19", "BL20", "BL21", "BL22", "BL23", "BL24", "BL25", "BL26", "BL27", "BL28", "BL29", "BL30", "BL31", "BL32", "BL33", "BL34", "BL35", "BL36", "BL37", "BL38", "BL39", "BL40", "BL41", "BL42", "BL43", "BL44", "BL45", "BL46", "BL47", "BL48", "BL49", "BL50", "BL51", "BL52", "BL53", "BL54", "BL55", "BL56", "BL57", "BL58", "BL59", "BL60", "BL61", "BL62", "BL63", "BL64", "BL65", "BL66", "BL67", "KI1", "KI2", "KI3", "KI4", "KI5", "KI6", "KI7", "KI8", "KI9", "KI10", "KI11", "KI12", "KI13", "KI14", "KI15", "KI16", "KI17", "KI18", "KI19", "KI20", "KI21", "KI22", "KI23", "KI24", "KI25", "KI26", "KI27", "PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7", "PC8", "PC9", "TE1", "TE2", "TE3", "TE4", "TE5", "TE6", "TE7", "TE8", "TE9", "TE10", "TE11", "TE12", "TE13", "TE14", "TE15", "TE16", "TE17", "TE18", "TE19", "TE20", "TE21", "TE22", "TE23", "GB1", "GB2", "GB3", "GB4", "GB5", "GB6", "GB7", "GB8", "GB9", "GB10", "GB11", "GB12", "GB13", "GB14", "GB15", "GB16", "GB17", "GB18", "GB19", "GB20", "GB21", "GB22", "GB23", "GB24", "GB25", "GB26", "GB27", "GB28", "GB29", "GB30", "GB31", "GB32", "GB33", "GB34", "GB35", "GB36", "GB37", "GB38", "GB39", "GB40", "GB41", "GB42", "GB43", "GB44", "LR1", "LR2", "LR3", "LR4", "LR5", "LR6", "LR7", "LR8", "LR9", "LR10", "LR11", "LR12", "LR13", "LR14", "GV1", "GV2", "GV3", "GV4", "GV5", "GV6", "GV7", "GV8", "GV9", "GV10", "GV11", "GV12", "GV13", "GV14", "GV15", "GV16", "GV17", "GV18", "GV19", "GV20", "GV21", "GV22", "GV23", "GV24", "GV25", "GV26", "GV27", "GV28", "CV1", "CV2", "CV3", "CV4", "CV5", "CV6", "CV7", "CV8", "CV9", "CV10", "CV11", "CV12", "CV13", "CV14", "CV15", "CV16", "CV17", "CV18", "CV19", "CV20", "CV21", "CV22", "CV23", "CV24"];
    const esc = value => String(value ?? '').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ICON = { sun: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>', moon: '<svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg>' };
const V3 = THREE.Vector3, D2R = Math.PI / 180, R2D = 180 / Math.PI, wrapD = d => ((d % 360) + 540) % 360 - 180;
// ===== 뷰어 =====
(function () {
  const $ = s => document.querySelector(s);
  const stage = $('#stage'), canvas = $('#gl'), labelsEl = $('#labels');
  const reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const MER = {}; MERIDIANS.forEach((m, k) => { m.k = k; m.points = []; MER[m.c] = m; });
  POINTS.forEach((p, i) => { p.i = i;  p.mid = p.mer === 'GV' || p.mer === 'CV'; MER[p.mer].points.push(i); });

  if (typeof THREE === 'undefined') throw new Error('3D 표시를 시작할 수 없습니다.');

  // ---------- 렌더러 ----------
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  const DPR = Math.min(window.devicePixelRatio || 1, 1.75);
  renderer.setPixelRatio(DPR);
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 1, 3000);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xa89c94, 0.72));
  const key = new THREE.DirectionalLight(0xffffff, 0.46); key.position.set(120, 260, 260); scene.add(key);
  const fill = new THREE.DirectionalLight(0xe8f0ff, 0.22); fill.position.set(-240, 60, 120); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffffff, 0.26); rim.position.set(0, 160, -300); scene.add(rim);

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xd0a891, roughness: 0.6, metalness: 0, side: THREE.DoubleSide });
  const vcMat = (r) => new THREE.MeshStandardMaterial({ vertexColors: true, roughness: r, metalness: 0, side: THREE.DoubleSide });
  const partMat = (hex, rough) => new THREE.MeshStandardMaterial({ color: hex, roughness: rough, metalness: 0 });
  const B64 = d => { const bin = atob(d), u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; };
  function buildLayer(buckets, mat) {
    const g = new THREE.Group(), meshes = [];
    buckets.forEach(b => {
      const u = B64(b.d), buf = u.buffer, pad = n => (n + 3) & ~3;
      let off = 0;
      const q = new Uint16Array(buf, off, b.n * 3); off += pad(b.n * 6);
      const nr = new Int8Array(buf, off, b.n * 3); off += pad(b.n * 3);
      let col = null; if (b.col) { col = new Uint8Array(buf, off, b.n * 3); off += pad(b.n * 3); }
      const ix = new Uint16Array(buf, off, b.m * 3);
      const pos = new Float32Array(b.n * 3);
      for (let i = 0; i < b.n; i++) for (let k = 0; k < 3; k++) pos[i * 3 + k] = b.lo[k] + q[i * 3 + k] / 65535 * b.rng[k];
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      const nf = new Float32Array(b.n * 3); for (let i = 0; i < nf.length; i++) nf[i] = nr[i] / 127;
      geo.setAttribute('normal', new THREE.BufferAttribute(nf, 3));
      if (col) { const cf = new Float32Array(b.n * 3); for (let i = 0; i < cf.length; i++) cf[i] = col[i] / 255; geo.setAttribute('color', new THREE.BufferAttribute(cf, 3)); }
      geo.setIndex(new THREE.BufferAttribute(ix, 1));
      geo.computeBoundingSphere();
      const m = new THREE.Mesh(geo, mat); g.add(m); meshes.push(m);
    });
    scene.add(g); return { g, meshes };
  }
  const bodyMeshes = [];
  const skinL = buildLayer(MODEL.skin, bodyMat); skinL.meshes.forEach(m => bodyMeshes.push(m));
  const L = { face: buildLayer(MODEL.face, vcMat(0.5)) };
  const LR = { bones: 0.55, muscle: 0.62, organs: 0.45, hair: 0.85 };
  function ensure(k) { if (!L[k]) { const mt = vcMat(LR[k]); if (k === 'hair') { mt.transparent = true; mt.opacity = 0.62; mt.depthWrite = false; } L[k] = buildLayer(MODEL[k], mt); } return L[k]; }
  L.face.meshes.forEach(m => { m.renderOrder = 0; });

  // ---------- 혈 인스턴스 ----------
  const INST = [], PINST = POINTS.map(() => []);
  PTD.forEach(r => {
    const pos = new V3(r[2], r[3], r[4]), nrm = new V3(r[5], r[6], r[7]);
    PINST[r[0]].push(INST.length);
    INST.push({ i: r[0], side: r[1], sh: r[8], pos, nrm, lp: pos.clone().addScaledVector(nrm, 0.25) });
  });
  const N = INST.length;
  const aPos = new Float32Array(N * 3), aCol = new Float32Array(N * 3), aSize = new Float32Array(N), aAlpha = new Float32Array(N);
  INST.forEach((t, k) => { aPos.set([t.lp.x, t.lp.y, t.lp.z], k * 3); });
  const ptGeo = new THREE.BufferGeometry();
  ptGeo.setAttribute('position', new THREE.BufferAttribute(aPos, 3));
  ptGeo.setAttribute('acol', new THREE.BufferAttribute(aCol, 3));
  ptGeo.setAttribute('asize', new THREE.BufferAttribute(aSize, 1));
  ptGeo.setAttribute('aalpha', new THREE.BufferAttribute(aAlpha, 1));
  const ptMat = new THREE.ShaderMaterial({
    uniforms: { uPR: { value: DPR }, uScale: { value: 1 } },
    vertexShader: `attribute vec3 acol; attribute float asize; attribute float aalpha; uniform float uPR; uniform float uScale;
      varying vec3 vC; varying float vA;
      void main(){ vC=acol; vA=aalpha; vec4 mv=modelViewMatrix*vec4(position,1.0); gl_Position=projectionMatrix*mv; gl_PointSize=asize*uScale*uPR; }`,
    fragmentShader: `varying vec3 vC; varying float vA;
      void main(){ vec2 c=gl_PointCoord-0.5; float d=length(c); if(d>0.5) discard;
        vec3 col = d>0.38 ? vec3(0.08,0.13,0.11) : (d>0.29 ? vec3(1.0) : vC);
        gl_FragColor=vec4(col, vA*smoothstep(0.5,0.43,d)); }`,
    transparent: true, depthWrite: false
  });
  const ptObj = new THREE.Points(ptGeo, ptMat); ptObj.renderOrder = 3; scene.add(ptObj);

  // 선택 표시 링
  const ringPos = new Float32Array(6), ringA = new Float32Array(2);
  const ringGeo = new THREE.BufferGeometry();
  ringGeo.setAttribute('position', new THREE.BufferAttribute(ringPos, 3));
  ringGeo.setAttribute('aalpha', new THREE.BufferAttribute(ringA, 1));
  const ringMat = new THREE.ShaderMaterial({
    uniforms: { uPR: { value: DPR }, uScale: { value: 1 }, uT: { value: 0 }, uCol: { value: new THREE.Color() } },
    vertexShader: `attribute float aalpha; uniform float uPR; uniform float uScale; uniform float uT; varying float vA;
      void main(){ vA=aalpha; vec4 mv=modelViewMatrix*vec4(position,1.0); gl_Position=projectionMatrix*mv; gl_PointSize=(30.0+4.0*uT)*uScale*uPR; }`,
    fragmentShader: `uniform vec3 uCol; varying float vA;
      void main(){ vec2 c=gl_PointCoord-0.5; float d=length(c); if(d>0.5||d<0.3) discard;
        vec3 col = d>0.42 ? vec3(0.08,0.13,0.11) : uCol; gl_FragColor=vec4(col, vA); }`,
    transparent: true, depthWrite: false, depthTest: false
  });
  const ringObj = new THREE.Points(ringGeo, ringMat); ringObj.renderOrder = 4; scene.add(ringObj);
  // 다중 강조(사암 보사·동씨 근처 표시)
  const HLMAX = 24, hlPos = new Float32Array(HLMAX * 3), hlCol = new Float32Array(HLMAX * 3), hlA = new Float32Array(HLMAX);
  const hlGeo = new THREE.BufferGeometry();
  hlGeo.setAttribute('position', new THREE.BufferAttribute(hlPos, 3));
  hlGeo.setAttribute('hcol', new THREE.BufferAttribute(hlCol, 3));
  hlGeo.setAttribute('aalpha', new THREE.BufferAttribute(hlA, 1));
  const hlMat = new THREE.ShaderMaterial({
    uniforms: { uPR: { value: DPR }, uScale: { value: 1 }, uT: { value: 0 } },
    vertexShader: `attribute vec3 hcol; attribute float aalpha; uniform float uPR; uniform float uScale; uniform float uT; varying vec3 vC; varying float vA;
      void main(){ vC=hcol; vA=aalpha; vec4 mv=modelViewMatrix*vec4(position,1.0); gl_Position=projectionMatrix*mv; gl_PointSize=(24.0+5.0*uT)*uScale*uPR; }`,
    fragmentShader: `varying vec3 vC; varying float vA;
      void main(){ vec2 c=gl_PointCoord-0.5; float d=length(c); if(d>0.5) discard;
        vec3 col = d>0.43 ? vec3(0.06,0.1,0.09) : (d>0.3 ? vC : (d>0.2 ? vec3(1.0) : vC));
        gl_FragColor=vec4(col, vA); }`,
    transparent: true, depthWrite: false, depthTest: false
  });
  const hlObj = new THREE.Points(hlGeo, hlMat); hlObj.renderOrder = 5; hlObj.frustumCulled = false; scene.add(hlObj); hlGeo.setDrawRange(0, 0);
  let HL = []; const VI = {}, gI = id => typeof id === 'number' ? INST[id] : VI[id], VP = { code: '', ko: '', mer: 'GV' };
  function focusAt(arr, mirror) {
    const sg = mirror ? -1 : 1, c = new V3(), n = new V3();
    arr.forEach(a => { c.add(new V3(a[0] * sg, a[1], a[2])); n.add(new V3(a[3] * sg, a[4], a[5])); }); c.multiplyScalar(1 / arr.length);
    let r = 0; arr.forEach(a => { r = Math.max(r, new V3(a[0] * sg, a[1], a[2]).distanceTo(c)); });
    if (n.length() < 0.35) n.set(arr[0][3] * sg, arr[0][4], arr[0][5]); n.normalize();
    goTo({ t: c, dist: Math.min(320, Math.max(44, r * 3.3 + 40)), theta: Math.atan2(n.x, n.z), phi: Math.min(2.6, Math.max(0.5, Math.acos(Math.max(-1, Math.min(1, n.y * 0.6))))) });
  }
  function setHighlight(items) {
    HL = []; const c = new THREE.Color();
    (items || []).forEach(it => {
      if (it.at) it.at.forEach((a, k) => { if (HL.length >= HLMAX) return; const sg = it.mirror ? -1 : 1, id = 'v' + HL.length; const pos = new V3(a[0] * sg, a[1], a[2]), nrm = new V3(a[3] * sg, a[4], a[5]); VI[id] = { v: 1, side: 0, pos, nrm, lp: pos.clone().addScaledVector(nrm, 0.25) }; HL.push({ id, col: it.col, tag: it.tag, text: it.text }); });
      else PINST[it.i].forEach(id => { if (HL.length < HLMAX && (!it.side || INST[id].side === it.side)) HL.push({ id, col: it.col, tag: it.tag, text: it.text }); });
    });
    HL.forEach((h, j) => { hlPos.set(gI(h.id).lp.toArray(), j * 3); c.set(h.col); hlCol.set([c.r, c.g, c.b], j * 3); });
    hlGeo.attributes.position.needsUpdate = hlGeo.attributes.hcol.needsUpdate = true; hlGeo.setDrawRange(0, HL.length);
  }
  function focusMany(idx, side) {
    side = side || 1;
    const ts = idx.map(i => INST[PINST[i].find(id => INST[id].side === side) ?? PINST[i][0]]);
    if (!ts.length) return;
    const c = new V3(), n = new V3(); ts.forEach(t => { c.add(t.pos); n.add(t.nrm); }); c.multiplyScalar(1 / ts.length);
    let r = 0; ts.forEach(t => { r = Math.max(r, t.pos.distanceTo(c)); });
    if (n.length() < 0.35) n.copy(ts[0].nrm); n.normalize();
    goTo({ t: c, dist: Math.min(320, Math.max(44, r * 3.3 + 40)), theta: Math.atan2(n.x, n.z), phi: Math.min(2.6, Math.max(0.5, Math.acos(Math.max(-1, Math.min(1, n.y * 0.6))))) });
  }


  // ---------- 경락선 ----------
  const lineObjs = {};
  const lineMats = {};
  MERIDIANS.forEach(m => {
    const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(m.col), transparent: true, opacity: 0.8, depthWrite: false });
    lineMats[m.c] = mat; lineObjs[m.c] = [];
    (LINES[m.c] || []).forEach(flat => {
      const pts = []; for (let k = 0; k < flat.length; k += 3) pts.push(new V3(flat[k], flat[k + 1], flat[k + 2]));
      if (pts.length < 2) return;
      const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
      const geo = new THREE.TubeGeometry(curve, Math.min(1400, pts.length * 2), 0.15, 5, false);
      const mesh = new THREE.Mesh(geo, mat); mesh.renderOrder = 2; scene.add(mesh); lineObjs[m.c].push(mesh);
    });
  });

  // ---------- 상태 ----------
  const state = { sel: null, filter: null, lines: true, labels: true, xray: false, bones: false, muscle: false, organs: false, hair: false };
  const internalOn = () => state.bones || state.muscle || state.organs;
  const seeThrough = () => state.xray || internalOn();
  const grey = new THREE.Color('#9aa39f');
  function paintPoints() {
    const c = new THREE.Color();
    INST.forEach((t, k) => {
      const p = POINTS[t.i], m = MER[p.mer];
      const inF = !state.filter || state.filter === p.mer;
      c.set(m.col); if (!inF) c.lerp(grey, 0.65);
      aCol.set([c.r, c.g, c.b], k * 3);
      aSize[k] = t.i === state.sel ? 12 : inF ? (state.filter ? 9 : 6.8) : 5;
      aAlpha[k] = inF ? 1 : 0.45;
    });
    ptGeo.attributes.acol.needsUpdate = ptGeo.attributes.asize.needsUpdate = ptGeo.attributes.aalpha.needsUpdate = true;
    MERIDIANS.forEach(m => {
      const on = !state.filter || state.filter === m.c;
      lineMats[m.c].opacity = state.filter ? (on ? 0.95 : 0.1) : 0.72;
      lineObjs[m.c].forEach(o => { o.visible = state.lines; });
    });
    if (state.sel !== null) {
      const ids = PINST[state.sel];
      ids.forEach((id, j) => ringPos.set(INST[id].lp.toArray(), j * 3));
      if (ids.length === 1) ringPos.set(INST[ids[0]].lp.toArray(), 3);
      ringGeo.attributes.position.needsUpdate = true;
      ringMat.uniforms.uCol.value.set(MER[POINTS[state.sel].mer].col);
    }
  }

  // ---------- 카메라 ----------
  const cam = { t: new V3(0, 88, 0), dist: 340, theta: 0, phi: Math.PI / 2 };
  let tween = null;
  function fitDist() {
    const a = camera.aspect || 1, tf = Math.tan(camera.fov * D2R / 2);
    return Math.max(96 / tf, 42 / (tf * a));
  }
  function goTo(goal, ms = 650) {
    const from = { t: cam.t.clone(), dist: cam.dist, theta: cam.theta, phi: cam.phi };
    const g = Object.assign({ t: cam.t.clone(), dist: cam.dist, theta: cam.theta, phi: cam.phi }, goal);
    g.theta = from.theta + wrapD((g.theta - from.theta) * R2D) * D2R;
    if (reduceMotion) ms = 1;
    tween = { from, g, t0: performance.now(), ms };
  }
  function stepTween(now) {
    if (!tween) return;
    let k = Math.min(1, (now - tween.t0) / tween.ms); const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
    const { from, g } = tween;
    cam.t.lerpVectors(from.t, g.t, e); cam.dist = from.dist + (g.dist - from.dist) * e;
    cam.theta = from.theta + (g.theta - from.theta) * e; cam.phi = from.phi + (g.phi - from.phi) * e;
    if (k >= 1) tween = null;
  }
  function applyCam() {
    const sp = Math.sin(cam.phi);
    camera.position.set(cam.t.x + cam.dist * sp * Math.sin(cam.theta), cam.t.y + cam.dist * Math.cos(cam.phi), cam.t.z + cam.dist * sp * Math.cos(cam.theta));
    camera.lookAt(cam.t);
  }
  const VIEWS = {
    full: () => ({ t: new V3(0, 88, 0), dist: fitDist(), theta: 0, phi: Math.PI / 2 }),
    front: () => ({ theta: 0, phi: Math.PI / 2 }),
    back: () => ({ theta: Math.PI, phi: Math.PI / 2 }),
    left: () => ({ theta: Math.PI / 2, phi: Math.PI / 2 }),
    right: () => ({ theta: -Math.PI / 2, phi: Math.PI / 2 }),
    head: () => ({ t: new V3(0, 158, 0), dist: 78, theta: 0.5, phi: 1.42 }),
  };
  function focusPoint(i) {
    const t = INST[PINST[i][0]], n = t.nrm.clone();
    const inward = -Math.sign(t.pos.x || 1) * n.x;
    if (Math.abs(t.pos.x) > 4 && inward > 0.3) n.z += n.z >= -0.1 ? 1.0 : -1.0;
    n.normalize();
    const k = t.sh || '';
    const close = /^(f\d|t\d|hn|ft|head|jaw|nose)/.test(k);
    goTo({ t: t.pos.clone(), dist: close ? 40 : 56, theta: Math.atan2(n.x, n.z), phi: Math.min(2.75, Math.max(0.3, Math.acos(Math.max(-1, Math.min(1, n.y))))) });
  }

  // ---------- 입력 ----------
  const ptrs = new Map(); let drag = null;
  canvas.addEventListener('contextmenu', e => e.preventDefault());
  canvas.addEventListener('pointerdown', e => {
    canvas.setPointerCapture(e.pointerId);
    ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    tween = null;
    drag = { x0: e.clientX, y0: e.clientY, moved: 0, t0: performance.now(), pan: e.button === 2 || e.shiftKey, multi: ptrs.size > 1 };
    canvas.classList.add('dragging');
  });
  canvas.addEventListener('pointermove', e => {
    const p = ptrs.get(e.pointerId); if (!p || !drag) return;
    const dx = e.clientX - p.x, dy = e.clientY - p.y;
    if (ptrs.size === 2) {
      const arr = [...ptrs.entries()];
      const other = arr.find(([id]) => id !== e.pointerId)[1];
      const d0 = Math.hypot(p.x - other.x, p.y - other.y), d1 = Math.hypot(e.clientX - other.x, e.clientY - other.y);
      if (d0 > 0 && d1 > 0) cam.dist = Math.min(560, Math.max(16, cam.dist * d0 / d1));
      pan(dx / 2, dy / 2); drag.multi = true;
    } else if (drag.pan) pan(dx, dy);
    else { cam.theta -= dx * 0.0075; cam.phi = Math.min(Math.PI - 0.1, Math.max(0.1, cam.phi - dy * 0.0075)); }
    drag.moved += Math.abs(dx) + Math.abs(dy);
    p.x = e.clientX; p.y = e.clientY;
  });
  function endPtr(e) {
    if (!ptrs.has(e.pointerId)) return;
    ptrs.delete(e.pointerId);
    if (drag && ptrs.size === 0) {
      if (drag.moved < 6 && !drag.multi && performance.now() - drag.t0 < 600) pick(e.clientX, e.clientY);
      drag = null; canvas.classList.remove('dragging');
    }
  }
  canvas.addEventListener('pointerup', endPtr);
  canvas.addEventListener('pointercancel', endPtr);
  canvas.addEventListener('wheel', e => { e.preventDefault(); tween = null; cam.dist = Math.min(560, Math.max(16, cam.dist * Math.exp(e.deltaY * 0.0012))); }, { passive: false });
  function pan(dx, dy) {
    const k = cam.dist * Math.tan(camera.fov * D2R / 2) * 2 / Math.max(1, stage.clientHeight);
    const right = new V3().setFromMatrixColumn(camera.matrix, 0), up = new V3().setFromMatrixColumn(camera.matrix, 1);
    cam.t.addScaledVector(right, -dx * k).addScaledVector(up, dy * k);
  }
  const ray = new THREE.Raycaster(), tmp = new V3();
  function screenOf(v) { tmp.copy(v).project(camera); return { x: (tmp.x + 1) / 2 * stage.clientWidth, y: (1 - tmp.y) / 2 * stage.clientHeight, z: tmp.z }; }
  function occluded(t) {
    if (seeThrough()) return false;
    const dir = t.lp.clone().sub(camera.position); const d = dir.length(); dir.normalize();
    ray.set(camera.position, dir); ray.far = d;
    const hit = ray.intersectObjects(bodyMeshes, false)[0];
    return hit && hit.distance < d - 0.7;
  }
  function pick(cx, cy) {
    const r = canvas.getBoundingClientRect(), x = cx - r.left, y = cy - r.top;
    const cand = [];
    INST.forEach((t, k) => {
      const s = screenOf(t.lp); if (s.z > 1) return;
      const d = Math.hypot(s.x - x, s.y - y);
      const p = POINTS[t.i];
      const w = state.filter && state.filter !== p.mer ? 6 : 0;
      if (d < 16) cand.push({ k, d: d + w });
    });
    cand.sort((a, b) => a.d - b.d);
    for (const c of cand) { if (!occluded(INST[c.k])) { select(INST[c.k].i); return; } }
  }

  // ---------- 라벨 ----------
  const labelPool = [];
  function labelEl(k) {
    if (!labelPool[k]) { const d = document.createElement('div'); d.className = 'lab'; labelsEl.appendChild(d); labelPool[k] = d; }
    return labelPool[k];
  }
  function updateLabels() {
    const W = stage.clientWidth, H = stage.clientHeight, placed = [];
    const list = [];
    const hlTag = {}; HL.forEach(h => { hlTag[h.id] = h; list.push(h.id); });
    if (state.sel !== null) PINST[state.sel].forEach(id => list.push(id));
    const seen = new Set();
    if (state.labels) {
      const src = state.filter ? MER[state.filter].points : (cam.dist < 150 ? POINTS.map(p => p.i) : []);
      src.forEach(i => { if (i !== state.sel) PINST[i].forEach(id => list.push(id)); });
    }
    let used = 0;
    const camPos = camera.position;
    for (const id of list) {
      if (seen.has(id)) continue; seen.add(id);
      const t = gI(id), hl = hlTag[id];
      if (!hl && t.i !== state.sel && t.pos.distanceTo(cam.t) > Math.max(34, cam.dist * 0.8)) continue;
      if (!seeThrough() && t.nrm.dot(tmp.copy(camPos).sub(t.pos)) <= 0) continue;
      const s = screenOf(t.lp);
      if (s.z > 1 || s.x < 8 || s.x > W - 8 || s.y < 30 || s.y > H - 8) continue;
      const p = t.v ? VP : POINTS[t.i], sel = t.i === state.sel || !!hl;
      const txt = hl ? (hl.text || (p.code + ' ' + p.ko)) : '';
      const w = hl ? ((hl.tag.length * 1.8 + txt.length * 1.4) * 6.6 + 22) : (p.code.length + p.ko.length * 1.8) * 6.6 + 18, h = 20;
      const rect = [s.x - w / 2, s.y - h - 8, s.x + w / 2, s.y - 8];
      if (!sel && placed.some(q => rect[0] < q[2] && rect[2] > q[0] && rect[1] < q[3] && rect[3] > q[1])) continue;
      placed.push(rect);
      if (used > 160) break;
      const el = labelEl(used++);
      const key = p.code + (hl ? '#' + hl.tag + hl.text : sel ? '*' : '');
      if (el.dataset.k !== key) {
        el.dataset.k = key; el.className = 'lab' + (hl ? ' sel hl' : sel ? ' sel' : '');
        el.style.setProperty('--mc', MER[p.mer].col); if (hl) el.style.setProperty('--hc', hl.col);
        el.innerHTML = hl ? '<b>' + esc(hl.tag) + '</b>' + esc(txt) : '<b>' + p.code + '</b>' + p.ko;
      }
      el.style.transform = `translate(${s.x.toFixed(1)}px,${s.y.toFixed(1)}px) translate(-50%,-150%)`;
      el.hidden = false;
    }
    for (let k = used; k < labelPool.length; k++) labelPool[k].hidden = true;
  }

  // ---------- 루프 ----------
  function resize() {
    const w = stage.clientWidth, h = stage.clientHeight;
    renderer.setSize(w, h, false); camera.aspect = w / Math.max(1, h); camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(stage); resize();
  cam.dist = fitDist();
  function frame(now) {
    stepTween(now); applyCam();
    const sc = Math.min(2.3, Math.max(1, Math.sqrt(300 / cam.dist)));
    ptMat.uniforms.uScale.value = sc; ringMat.uniforms.uScale.value = sc;
    ringMat.uniforms.uT.value = reduceMotion ? 0.5 : (Math.sin(now / 260) + 1) / 2;
    if (state.sel !== null) {
      PINST[state.sel].forEach((id, j) => {
        const t = INST[id];
        ringA[j] = (seeThrough() || t.nrm.dot(tmp.copy(camera.position).sub(t.pos)) > 0) ? 1 : 0;
      });
      if (PINST[state.sel].length === 1) ringA[1] = 0;
      ringGeo.attributes.aalpha.needsUpdate = true;
    }
    hlMat.uniforms.uScale.value = sc; hlMat.uniforms.uT.value = ringMat.uniforms.uT.value;
    HL.forEach((h, j) => { const t = gI(h.id); hlA[j] = (seeThrough() || t.nrm.dot(tmp.copy(camera.position).sub(t.pos)) > 0) ? 1 : 0.28; });
    if (HL.length) hlGeo.attributes.aalpha.needsUpdate = true;
    renderer.render(scene, camera);
    updateLabels();
    requestAnimationFrame(frame);
  }

  // ---------- UI ----------
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const chipsEl = $('#chips');
  function renderChips() {
    chipsEl.innerHTML = `<button class="chip" data-m="" aria-pressed="${!state.filter}">전체</button>` +
      MERIDIANS.map(m => `<button class="chip" data-m="${m.c}" style="--mc:${m.col}" aria-pressed="${state.filter === m.c}" title="${m.ko} ${m.hz}"><i></i>${m.short}<small>${m.c}</small></button>`).join('');
  }
  chipsEl.addEventListener('click', e => { const b = e.target.closest('.chip'); if (b) setFilter(b.dataset.m || null); });
  function setFilter(c) { state.filter = c; renderChips(); paintPoints(); renderList(); }

  const detailEl = $('#detail');
  function emptyHtml(msg) { return `<div class="empty-card"><b>${msg}</b><p>모형의 혈 점을 누르거나, 위 검색창과 경락 버튼으로 고르세요.</p></div>`; }
  function resetView() {
    setHighlight([]); state.sel = null; ringA.fill(0); ringGeo.attributes.aalpha.needsUpdate = true;
    setFilter(null); renderDetail();
    const fb = document.querySelector('[data-view=full]'); if (fb) { fb.classList.add('pressing'); setTimeout(() => fb.classList.remove('pressing'), 380); fb.click(); }
    window.dispatchEvent(new Event('acu:reset'));
  }
  function renderDetail() {
    if (state.sel === null) { detailEl.innerHTML = emptyHtml('경혈을 선택하세요'); return; }
    const p = POINTS[state.sel], m = MER[p.mer], arr = m.points, pos = arr.indexOf(p.i);
    const prev = pos > 0 ? POINTS[arr[pos - 1]] : null, next = pos < arr.length - 1 ? POINTS[arr[pos + 1]] : null;
    detailEl.style.setProperty('--mc', m.col);
    detailEl.innerHTML = `
      <div class="d-top"><button class="xbtn" data-x="1" aria-label="선택 해제하고 전신으로" title="선택 해제 · 전신 보기">×</button><span class="code">${p.code}</span><button class="merlink" data-m="${m.c}">${m.ko} ${m.hz}</button><span class="side">${p.mid ? '정중선 · 단혈' : '좌우 양측'}</span></div>
      <div class="d-name"><span class="hz">${p.hz}</span><span class="ko">${p.ko}</span></div>
      ${p.tags.length ? `<div class="tags">${p.tags.map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div>` : ''}
      <dl><dt>위치</dt><dd>${esc(p.loc)}</dd><dt>주치</dt><dd>${esc(p.ind)}</dd>${p.note ? `<dt>주의</dt><dd class="warn">${esc(p.note)}</dd>` : ''}</dl>
      <p class="approx">모형의 점은 근사 위치입니다. 위의 표준 위치 설명과 해부학적 표지를 함께 확인하세요.</p>
      <div class="archive-links"><a data-archive-link href="${esc(p.href)}" target="_top">위치·주치·배혈 상세 문서 →</a><a href="${esc(p.route)}" target="_top">경락 경로 읽기 →</a><a href="${esc(p.dailyHref)}" target="_top">하루 경혈 카드 →</a></div>
      <details class="source-info"><summary>주치·활용의 자료 출처</summary>${p.rows.map(row => `<p><b>${esc(row.layer)}</b> · ${esc(row.label)}<br>${esc(row.text)}<br>${row.source ? `<a href="${esc(row.source)}" target="_blank" rel="noopener noreferrer">원자료 확인 ↗</a>` : ''}</p>`).join('')}<a href="${esc(p.standardReference)}" target="_blank" rel="noopener noreferrer">KMCRIC 표준경혈 DB ↗</a></details>
      <div class="d-nav">
        <button data-go="${prev ? prev.i : ''}" ${prev ? '' : 'disabled'}>← ${prev ? prev.code + ' ' + prev.ko : '처음'}</button>
        <button class="go" data-focus="1">모형에서 보기</button>
        <button data-go="${next ? next.i : ''}" ${next ? '' : 'disabled'}>${next ? next.code + ' ' + next.ko : '마지막'} →</button>
      </div>`;
  }
  detailEl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.x) { resetView(); return; }
    if (b.dataset.layers) { ['tMuscle', 'tBones'].forEach(id => { const x = document.getElementById(id); if (x && x.getAttribute('aria-pressed') !== 'true') x.click(); }); }
    else if (b.dataset.m) setFilter(b.dataset.m);
    else if (b.dataset.focus) { focusPoint(state.sel); showStage(); }
    else if (b.dataset.go !== undefined && b.dataset.go !== '') { select(+b.dataset.go, { focus: true }); }
  });

  const listEl = $('#list'), listTitle = $('#listTitle');
  function renderList() {
    const mc = state.filter || (state.sel !== null ? POINTS[state.sel].mer : 'LU'), m = MER[mc];
    listTitle.innerHTML = `${m.ko} <span>${m.hz} · ${m.points.length}혈</span>`;
    listEl.innerHTML = m.points.map(i => { const p = POINTS[i]; return `<li><button data-i="${i}" class="${i === state.sel ? 'on' : ''}"><span class="lc">${p.code}</span>${p.ko}<span class="lh">${p.hz}</span></button></li>`; }).join('');
  }
  listEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b) select(+b.dataset.i, { focus: true }); });

  function showStage() {
    if (window.innerWidth <= 860) { const r = stage.getBoundingClientRect(); if (r.bottom < 80 || r.top < -r.height / 2) stage.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' }); }
  }
  function select(i, opt = {}) {
    if (!opt.keepHL) setHighlight([]);
    if (!Number.isInteger(i) || i < 0 || i >= POINTS.length) return;
    state.sel = i; paintPoints(); renderDetail(); renderList();
    const selected = POINTS[i];
    const url = new URL(window.location.href); url.searchParams.set('point', selected.code);
    history.replaceState(null, '', url);
    if (window.parent !== window) window.parent.postMessage({type:'minseong-acupoint-select',code:selected.code}, window.location.origin);
    if (opt.focus) { focusPoint(i); showStage(); }
  }

  // 검색
  const qEl = $('#q'), resEl = $('#results'); let hits = [], kb = -1;
  function search(raw) {
    raw = raw.trim(); if (!raw) return [];
    const nq = raw.toLowerCase().replace(/[\s\-.]/g, '');
    const out = [];
    POINTS.forEach(p => {
      let sc = 0, why = '';
      const code = p.code.toLowerCase();
      if (code === nq) sc = 100;
      else if (/^[a-z]{2}\d*$/.test(nq) && code.startsWith(nq)) sc = 80;
      if (p.ko === raw) sc = Math.max(sc, 96); else if (p.ko.includes(raw)) sc = Math.max(sc, 70);
      if (p.hz.includes(raw)) sc = Math.max(sc, 90);
      if (!sc && raw.length >= 2) {
        if (p.ind.includes(raw)) { sc = 40; why = '주치 · ' + p.ind; }
        else if (p.loc.includes(raw)) { sc = 25; why = '위치 · ' + p.loc; }
        else if (p.tags.some(t => t.includes(raw))) { sc = 30; why = p.tags.join(' · '); }
        else {
          const a = window.ANAT && window.ANAT[p.code];
          if (a) for (const [k, lab] of [['m', '근육'], ['n', '신경'], ['v', '혈관'], ['b', '뼈']]) {
            const arr = [].concat(a[k] || []);
            if (arr.some(x => String(x).includes(raw))) { sc = 35; why = lab + ' · ' + arr.join(' · '); break; }
          }
        }
      }
      if (!sc && p.search.toLowerCase().includes(raw.toLowerCase())) { sc=25; why='아카이브 위치·주치·분류'; }
      if (sc) out.push({ i: p.i, sc, why });
    });
    out.sort((a, b) => b.sc - a.sc || a.i - b.i);
    return out.slice(0, 60);
  }
  function renderResults() {
    const v = qEl.value.trim();
    if (!v) { resEl.hidden = true; return; }
    hits = search(v); kb = hits.length ? 0 : -1;
    resEl.innerHTML = hits.length ? hits.map((h, k) => {
      const p = POINTS[h.i], m = MER[p.mer];
      return `<li><button data-i="${p.i}" class="${k === kb ? 'kb' : ''}" style="--mc:${m.col}"><span class="rc">${p.code}</span><span class="rn">${p.ko} <span style="font-family:var(--font-display)">${p.hz}</span></span><span class="rm">${esc(h.why || m.ko)}</span></button></li>`;
    }).join('') : `<li class="empty">‘${esc(v)}’에 맞는 혈이 없습니다. 혈명, 한자, 코드(ST36), 증상, 근육·신경·혈관·뼈 이름으로 찾아보세요.</li>`;
    resEl.hidden = false;
  }
  qEl.addEventListener('input', renderResults);
  qEl.addEventListener('focus', () => { if (qEl.value.trim()) renderResults(); });
  qEl.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      if (!hits.length) return; e.preventDefault();
      kb = (kb + (e.key === 'ArrowDown' ? 1 : -1) + hits.length) % hits.length;
      [...resEl.querySelectorAll('button')].forEach((b, k) => { b.classList.toggle('kb', k === kb); if (k === kb) b.scrollIntoView({ block: 'nearest' }); });
    } else if (e.key === 'Enter') { if (kb >= 0 && hits[kb]) { pickResult(hits[kb].i); } }
    else if (e.key === 'Escape') { resEl.hidden = true; }
  });
  resEl.addEventListener('pointerdown', e => e.preventDefault());
  resEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b) pickResult(+b.dataset.i); });
  function pickResult(i) { resEl.hidden = true; qEl.blur(); select(i, { focus: true }); }
  document.addEventListener('pointerdown', e => { if (!e.target.closest('.search')) resEl.hidden = true; });

  // 보기·토글
  document.querySelector('.views').addEventListener('click', e => { const b = e.target.closest('[data-view]'); if (b) goTo(VIEWS[b.dataset.view]()); });
  function toggle(id, keyName, fn) {
    const b = $(id); b.addEventListener('click', () => { state[keyName] = !state[keyName]; b.setAttribute('aria-pressed', state[keyName]); fn && fn(); });
  }
  toggle('#tLines', 'lines', paintPoints);
  toggle('#tLabels', 'labels');
  function updateSkin() {
    const t = seeThrough();
    bodyMat.transparent = t; bodyMat.opacity = internalOn() ? 0.13 : state.xray ? 0.32 : 1; bodyMat.depthWrite = !t; bodyMat.needsUpdate = true;
    ['bones', 'muscle', 'organs', 'hair'].forEach(k => { if (state[k]) ensure(k).g.visible = true; else if (L[k]) L[k].g.visible = false; });
    L.face.g.visible = !internalOn() || state.xray ? true : false;
  }
  toggle('#tXray', 'xray', updateSkin);
  toggle('#tBones', 'bones', updateSkin);
  toggle('#tMuscle', 'muscle', updateSkin);
  toggle('#tOrgans', 'organs', updateSkin);
  toggle('#tHair', 'hair', updateSkin);
  const root = document.documentElement, tb = $('#tTheme'), mq = window.matchMedia('(prefers-color-scheme: dark)');
  const curTheme = () => root.dataset.theme || (mq.matches ? 'dark' : 'light');
  function paintTheme() { const d = curTheme() === 'dark'; tb.innerHTML = (d ? ICON.sun : ICON.moon) + (d ? '라이트' : '다크'); tb.setAttribute('aria-label', d ? '라이트 모드로 전환' : '다크 모드로 전환'); }
  try { const sv = localStorage.getItem('acuTheme'); if (sv === 'dark' || sv === 'light') root.dataset.theme = sv; } catch (e) {}
  tb.addEventListener('click', () => { root.dataset.theme = curTheme() === 'dark' ? 'light' : 'dark'; try { localStorage.setItem('acuTheme', root.dataset.theme); } catch (e) {} paintTheme(); });
  mq.addEventListener && mq.addEventListener('change', paintTheme);
  paintTheme();
  window.__acu = { cam, goTo, VIEWS, select: i => select(i, { focus: true }), setFilter, state, updateSkin, INST, resetView, emptyHtml, setHighlight, focusMany, focusAt, MER, PINST, showStage, selectRaw: select, hideSel() { state.sel = null; ringA.fill(0); ringGeo.attributes.aalpha.needsUpdate = true; paintPoints(); } };

  // 시작 상태: 족삼리 선택, 전신 정면
  renderChips();
  const initialCode = (new URL(location.href).searchParams.get('point') || 'ST36').toUpperCase();
  const initial = POINTS.findIndex(p => p.code === initialCode);
  select(initial < 0 ? POINTS.findIndex(p => p.code === 'ST36') : initial);
  document.getElementById('today-point').addEventListener('click', () => {
    const now = new Date(), kst = new Date(now.getTime()+9*60*60*1000);
    const day = Math.floor((Date.UTC(kst.getUTCFullYear(),kst.getUTCMonth(),kst.getUTCDate())-Date.UTC(kst.getUTCFullYear(),0,1))/86400000);
    const todayCode = DAILY_CODES[((day % DAILY_CODES.length)+DAILY_CODES.length)%DAILY_CODES.length];
    select(POINTS.findIndex(p => p.code === todayCode),{focus:true});
  });
  document.getElementById('share-point').addEventListener('click', async () => {
    if (state.sel === null) return;
    const url = new URL('/acupoint-network/3d-map/',location.origin); url.searchParams.set('point',POINTS[state.sel].code);
    const status = document.getElementById('share-status');
    try { await navigator.clipboard.writeText(url.href); status.textContent='선택한 경혈 링크를 복사했습니다.'; }
    catch (_) { const input=document.getElementById('share-fallback'); input.hidden=false; input.value=url.href; input.select(); status.textContent='아래 주소를 복사하세요.'; }
  });
  $('#loading').remove();
  requestAnimationFrame(frame);
})();


  } catch (error) {
    const loading=document.getElementById('loading');
    if(loading) { loading.replaceChildren(); const text=document.createElement('p'); text.textContent='3D 표시를 불러오지 못했습니다. 새로고침하거나 2D 경혈 아틀라스를 이용하세요.'; const link=document.createElement('a');link.href='/acupoint-network/standard-atlas/';link.target='_top';link.textContent='2D 경혈 아틀라스 열기 →';loading.append(text,link); }
    console.error('3D 경혈 지도:',error.message);
  }
})();
