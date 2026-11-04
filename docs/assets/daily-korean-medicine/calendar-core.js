/*
Local calendar calculations. Upstream licenses and notices:

MIT License

Copyright (c) 2022 Jinil Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

SunCalc astronomical position/illumination subset:
Copyright (c) 2026, Volodymyr Agafonkin
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/
(function(root,factory){const api=factory();if(typeof module==="object"&&module.exports)module.exports=api;else root.MinseongCalendar=api;})(typeof window==="undefined"?globalThis:window,function(){"use strict";
const LUNAR_CALENDAR_DATA = {
  KOREAN_LUNAR_MIN_VALUE: 10000101,
  KOREAN_LUNAR_MAX_VALUE: 20501118,
  KOREAN_SOLAR_MIN_VALUE: 10000213,
  KOREAN_SOLAR_MAX_VALUE: 20501231,

  KOREAN_LUNAR_BASE_YEAR: 1000,
  SOLAR_LUNAR_DAY_DIFF: 43,

  LUNAR_SMALL_MONTH_DAY: 29,
  LUNAR_BIG_MONTH_DAY: 30,
  SOLAR_SMALL_YEAR_DAY: 365,
  SOLAR_BIG_YEAR_DAY: 366,

  SOLAR_DAYS: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 29],

  KOREAN_CHEONGAN: [
    0xac11, 0xc744, 0xbcd1, 0xc815, 0xbb34, 0xae30, 0xacbd, 0xc2e0, 0xc784,
    0xacc4,
  ].map((c) => String.fromCharCode(c)),
  KOREAN_GANJI: [
    0xc790, 0xcd95, 0xc778, 0xbb18, 0xc9c4, 0xc0ac, 0xc624, 0xbbf8, 0xc2e0,
    0xc720, 0xc220, 0xd574,
  ].map((c) => String.fromCharCode(c)),
  KOREAN_GAPJA_UNIT: [0xb144, 0xc6d4, 0xc77c].map((c) =>
    String.fromCharCode(c),
  ),

  CHINESE_CHEONGAN: [
    0x7532, 0x4e59, 0x4e19, 0x4e01, 0x620a, 0x5df1, 0x5e9a, 0x8f9b, 0x58ec,
    0x7678,
  ].map((c) => String.fromCharCode(c)),
  CHINESE_GANJI: [
    0x5b50, 0x4e11, 0x5bc5, 0x536f, 0x8fb0, 0x5df3, 0x5348, 0x672a, 0x7533,
    0x9149, 0x620c, 0x4ea5,
  ].map((c) => String.fromCharCode(c)),
  CHINESE_GAPJA_UNIT: [0x5e74, 0x6708, 0x65e5].map((c) =>
    String.fromCharCode(c),
  ),

  INTERCALATION_STR: [0xc724, 0x958f].map((c) => String.fromCharCode(c)),

  KOREAN_LUNAR_DATA: [
    0x82c60a57, 0x82fec52b, 0x82c40d2a, 0x82c60d55, 0xc30095ad, 0x82c4056a,
    0x82c6096d, 0x830054dd, 0xc2c404ad, 0x82c40a4d, 0x83002e4d, 0x82c40b26,
    0xc300ab56, 0x82c60ad5, 0x82c4035a, 0x8300697a, 0xc2c6095b, 0x82c4049b,
    0x83004a9b, 0x82c40a4b, 0xc301caa5, 0x82c406aa, 0x82c60ad5, 0x830092dd,
    0xc2c402b5, 0x82c60957, 0x82fe54ae, 0x82c60c97, 0xc2c4064b, 0x82ff254a,
    0x82c60da9, 0x8300a6b6, 0xc2c6066d, 0x82c4026e, 0x8301692e, 0x82c4092e,
    0xc2c40c96, 0x83004d95, 0x82c40d4a, 0x8300cd69, 0xc2c40b58, 0x82c80d6b,
    0x8301926b, 0x82c4025d, 0xc2c4092b, 0x83005aab, 0x82c40a95, 0x82c40b4a,
    0xc3021eab, 0x82c402d5, 0x8301b55a, 0x82c604bb, 0xc2c4025b, 0x83007537,
    0x82c4052b, 0x82c40695, 0xc3003755, 0x82c406aa, 0x8303cab5, 0x82c40275,
    0xc2c404b6, 0x83008a5e, 0x82c40a56, 0x82c40d26, 0xc3005ea6, 0x82c60d55,
    0x82c405aa, 0x83001d6a, 0xc2c6096d, 0x8300b4af, 0x82c4049d, 0x82c40a4d,
    0xc3007d2d, 0x82c40aa6, 0x82c60b55, 0x830045d5, 0xc2c4035a, 0x82c6095d,
    0x83011173, 0x82c4045b, 0xc3009a4f, 0x82c4064b, 0x82c40aa5, 0x83006b69,
    0xc2c606b5, 0x82c402da, 0x83002ab6, 0x82c60937, 0xc2fec497, 0x82c60c97,
    0x82c4064b, 0x82fe86aa, 0xc2c60da5, 0x82c405b4, 0x83034a6d, 0x82c402ae,
    0xc2c40e61, 0x83002d2e, 0x82c40c96, 0x83009d4d, 0x82c40d4a, 0x82c60d65,
    0x83016595, 0x82c6055d, 0xc2c4026d, 0x83002a5d, 0x82c4092b, 0x8300aa97,
    0xc2c40a95, 0x82c40b4a, 0x83008b5a, 0x82c60ad5, 0xc2c6055b, 0x830042b7,
    0x82c40457, 0x82c4052b, 0xc3001d2b, 0x82c40695, 0x8300972d, 0x82c405aa,
    0xc2c60ab5, 0x830054ed, 0x82c404b6, 0x82c60a57, 0xc2ff344e, 0x82c40d26,
    0x8301be92, 0x82c60d55, 0xc2c405aa, 0x830089ba, 0x82c6096d, 0x82c404ae,
    0xc3004a9d, 0x82c40a4d, 0x82c40d25, 0x83002f25, 0xc2c40b54, 0x8303ad69,
    0x82c402da, 0x82c6095d, 0xc301649b, 0x82c4049b, 0x82c40a4b, 0x83004b4b,
    0xc2c406a5, 0x8300bb53, 0x82c406b4, 0x82c60ab6, 0xc3018956, 0x82c60997,
    0x82c40497, 0x83004697, 0xc2c4054b, 0x82fec6a5, 0x82c60da5, 0x82c405ac,
    0xc303aab5, 0x82c4026e, 0x82c4092e, 0x83006cae, 0xc2c40c96, 0x82c40d4a,
    0x83002f4a, 0x82c60d55, 0xc300b56b, 0x82c6055b, 0x82c4025d, 0x8300793d,
    0xc2c40927, 0x82c40a95, 0x83015d15, 0x82c40b4a, 0xc2c60b55, 0x830112d5,
    0x82c604db, 0x82fe925e, 0xc2c60a57, 0x82c4052b, 0x83006aab, 0x82c40695,
    0xc2c406aa, 0x83003baa, 0x82c60ab5, 0x8300b4b7, 0xc2c404ae, 0x82c60a57,
    0x82fe752e, 0x82c40d26, 0xc2c60e93, 0x830056d5, 0x82c405aa, 0x82c609b5,
    0xc300256d, 0x82c404ae, 0x8301aa4d, 0x82c40a4d, 0xc2c40d26, 0x83006d65,
    0x82c40b52, 0x82c60d6a, 0xc30026da, 0x82c6095d, 0x8301c49d, 0x82c4049b,
    0xc2c40a4b, 0x83008aab, 0x82c406a5, 0x82c40b54, 0xc3004bb4, 0x82c60ab6,
    0x82c6095b, 0x83002537, 0xc2c40497, 0x8300964f, 0x82c4054b, 0x82c406a5,
    0xc30176c5, 0x82c405ac, 0x82c60ab6, 0x8301386e, 0xc2c4092e, 0x8300cc97,
    0x82c40c96, 0x82c40d4a, 0xc3008daa, 0x82c60b55, 0x82c4056a, 0x83025adb,
    0xc2c4025d, 0x82c4092e, 0x83002d2b, 0x82c40a95, 0xc3009d4d, 0x82c40b2a,
    0x82c60b55, 0x83007575, 0xc2c404da, 0x82c60a5b, 0x83004557, 0x82c4052b,
    0xc301ca93, 0x82c40693, 0x82c406aa, 0x83008ada, 0xc2c60ae5, 0x82c404b6,
    0x83004aae, 0x82c60a57, 0xc2c40527, 0x82ff2526, 0x82c60e53, 0x8300a6cb,
    0xc2c405aa, 0x82c605ad, 0x830164ad, 0x82c404ae, 0xc2c40a4e, 0x83004d4d,
    0x82c40d26, 0x8300bd53, 0xc2c40b52, 0x82c60b6a, 0x8301956a, 0x82c60557,
    0xc2c4049d, 0x83015a1b, 0x82c40a4b, 0x82c40aa5, 0xc3001ea5, 0x82c40b52,
    0x8300bb5a, 0x82c60ab6, 0xc2c6095b, 0x830064b7, 0x82c40497, 0x82c4064b,
    0xc300374b, 0x82c406a5, 0x8300b6b3, 0x82c405ac, 0xc2c60ab6, 0x830182ad,
    0x82c4049e, 0x82c40a4d, 0xc3005d4b, 0x82c40b25, 0x82c40b52, 0x83012e52,
    0xc2c60b5a, 0x8300a95e, 0x82c6095b, 0x82c4049b, 0xc3006a57, 0x82c40a4b,
    0x82c40aa5, 0x83004ba5, 0xc2c406d4, 0x8300cad6, 0x82c60ab6, 0x82c60937,
    0x8300849f, 0x82c40497, 0x82c4064b, 0x82fe56ca, 0xc2c60da5, 0x82c405aa,
    0x83001d6c, 0x82c60a6e, 0xc300b92f, 0x82c4092e, 0x82c40c96, 0x83007d55,
    0xc2c40d4a, 0x82c60d55, 0x83013555, 0x82c4056a, 0xc2c60a6d, 0x83001a5d,
    0x82c4092b, 0x83008a5b, 0xc2c40a95, 0x82c40b2a, 0x83015b2a, 0x82c60ad5,
    0xc2c404da, 0x83001cba, 0x82c60a57, 0x8300952f, 0xc2c40527, 0x82c40693,
    0x830076b3, 0x82c406aa, 0xc2c60ab5, 0x83003575, 0x82c404b6, 0x8300ca67,
    0xc2c40a2e, 0x82c40d16, 0x83008e96, 0x82c40d4a, 0xc2c60daa, 0x830055ea,
    0x82c6056d, 0x82c404ae, 0xc301285d, 0x82c40a2d, 0x8300ad17, 0x82c40aa5,
    0xc2c40b52, 0x83007d74, 0x82c60ada, 0x82c6055d, 0xc300353b, 0x82c4045b,
    0x82c40a2b, 0x83011a2b, 0xc2c40aa5, 0x83009b55, 0x82c406b2, 0x82c60ad6,
    0xc3015536, 0x82c60937, 0x82c40457, 0x83003a57, 0xc2c4052b, 0x82feaaa6,
    0x82c60d95, 0x82c405aa, 0xc3017aac, 0x82c60a6e, 0x82c4052e, 0x83003cae,
    0xc2c40a56, 0x8300bd2b, 0x82c40d2a, 0x82c60d55, 0xc30095ad, 0x82c4056a,
    0x82c60a6d, 0x8300555d, 0xc2c4052b, 0x82c40a8d, 0x83002e55, 0x82c40b2a,
    0xc300ab56, 0x82c60ad5, 0x82c404da, 0x83006a7a, 0xc2c60a57, 0x82c4051b,
    0x83014a17, 0x82c40653, 0xc301c6a9, 0x82c405aa, 0x82c60ab5, 0x830092bd,
    0xc2c402b6, 0x82c60a37, 0x82fe552e, 0x82c40d16, 0x82c60e4b, 0x82fe3752,
    0x82c60daa, 0x8301b5b4, 0xc2c6056d, 0x82c402ae, 0x83007a3d, 0x82c40a2d,
    0xc2c40d15, 0x83004d95, 0x82c40b52, 0x8300cb69, 0xc2c60ada, 0x82c6055d,
    0x8301925b, 0x82c4045b, 0xc2c40a2b, 0x83005aab, 0x82c40a95, 0x82c40b52,
    0xc3001eaa, 0x82c60ab6, 0x8300c55b, 0x82c604b7, 0xc2c40457, 0x83007537,
    0x82c4052b, 0x82c40695, 0xc3014695, 0x82c405aa, 0x8300cab5, 0x82c60a6e,
    0xc2c404ae, 0x83008a5e, 0x82c40a56, 0x82c40d2a, 0xc3006eaa, 0x82c60d55,
    0x82c4056a, 0x8301295a, 0xc2c6095d, 0x8300b4af, 0x82c4049b, 0x82c40a4d,
    0xc3007d2d, 0x82c40b2a, 0x82c60b55, 0x830045d5, 0xc2c402da, 0x82c6095b,
    0x83011157, 0x82c4049b, 0xc3009a4f, 0x82c4064b, 0x82c406a9, 0x83006aea,
    0xc2c606b5, 0x82c402b6, 0x83002aae, 0x82c60937, 0xc2ffb496, 0x82c40c96,
    0x82c60e4b, 0x82fe76b2, 0xc2c60daa, 0x82c605ad, 0x8300336d, 0x82c4026e,
    0xc2c4092e, 0x83002d2d, 0x82c40c95, 0x83009d4d, 0xc2c40b4a, 0x82c60b69,
    0x8301655a, 0x82c6055b, 0xc2c4025d, 0x83002a5b, 0x82c4092b, 0x8300aa97,
    0xc2c40695, 0x82c4074a, 0x83008b5a, 0x82c60ab6, 0xc2c6053b, 0x830042b7,
    0x82c40257, 0x82c4052b, 0xc3001d2b, 0x82c40695, 0x830096ad, 0x82c405aa,
    0xc2c60ab5, 0x830054ed, 0x82c404ae, 0x82c60a57, 0xc2ff344e, 0x82c40d2a,
    0x8301bd94, 0x82c60b55, 0x82c4056a, 0x8300797a, 0x82c6095d, 0x82c404ae,
    0xc3004a9b, 0x82c40a4d, 0x82c40d25, 0x83011aaa, 0xc2c60b55, 0x8300956d,
    0x82c402da, 0x82c6095b, 0xc30054b7, 0x82c40497, 0x82c40a4b, 0x83004b4b,
    0xc2c406a9, 0x8300cad5, 0x82c605b5, 0x82c402b6, 0xc300895e, 0x82c6092f,
    0x82c40497, 0x82fe4696, 0xc2c40d4a, 0x8300cea5, 0x82c60d69, 0x82c6056d,
    0xc301a2b5, 0x82c4026e, 0x82c4092e, 0x83006cad, 0xc2c40c95, 0x82c40d4a,
    0x83002f4a, 0x82c60b59, 0xc300c56d, 0x82c6055b, 0x82c4025d, 0x8300793b,
    0xc2c4092b, 0x82c40a95, 0x83015b15, 0x82c406ca, 0xc2c60ad5, 0x830112b6,
    0x82c604bb, 0x8300925f, 0xc2c40257, 0x82c4052b, 0x82fe6aaa, 0x82c60e95,
    0xc2c406aa, 0x83003baa, 0x82c60ab5, 0x8300b4b7, 0xc2c404ae, 0x82c60a57,
    0x82fe752d, 0x82c40d26, 0xc2c60d95, 0x830055d5, 0x82c4056a, 0x82c6096d,
    0xc300255d, 0x82c404ae, 0x8300aa4f, 0x82c40a4d, 0xc2c40d25, 0x83006d69,
    0x82c60b55, 0x82c4035a, 0xc3002aba, 0x82c6095b, 0x8301c49b, 0x82c40497,
    0xc2c40a4b, 0x83008b2b, 0x82c406a5, 0x82c406d4, 0xc3034ab5, 0x82c402b6,
    0x82c60937, 0x8300252f, 0xc2c40497, 0x82fe964e, 0x82c40d4a, 0x82c60ea5,
    0xc30166a9, 0x82c6056d, 0x82c402b6, 0x8301385e, 0xc2c4092e, 0x8300bc97,
    0x82c40a95, 0x82c40d4a, 0xc3008daa, 0x82c60b4d, 0x82c6056b, 0x830042db,
    0xc2c4025d, 0x82c4092d, 0x83002d2b, 0x82c40a95, 0xc3009b4d, 0x82c406aa,
    0x82c60ad5, 0x83006575, 0xc2c604bb, 0x82c4025b, 0x83013457, 0x82c4052b,
    0xc2ffba94, 0x82c60e95, 0x82c406aa, 0x83008ada, 0xc2c609b5, 0x82c404b6,
    0x83004aae, 0x82c60a4f, 0xc2c20526, 0x83012d26, 0x82c60d55, 0x8301a5a9,
    0xc2c4056a, 0x82c6096d, 0x8301649d, 0x82c4049e, 0xc2c40a4d, 0x83004d4d,
    0x82c40d25, 0x8300bd53, 0xc2c40b54, 0x82c60b5a, 0x8301895a, 0x82c6095b,
    0xc2c4049b, 0x83004a97, 0x82c40a4b, 0x82c40aa5, 0xc3001ea5, 0x82c406d4,
    0x8302badb, 0x82c402b6, 0xc2c60937, 0x830064af, 0x82c40497, 0x82c4064b,
    0xc2fe374a, 0x82c60da5, 0x8300b6b5, 0x82c6056d, 0xc2c402ae, 0x8300793e,
    0x82c4092e, 0x82c40c96, 0xc3015d15, 0x82c40d4a, 0x82c60da5, 0x83013555,
    0xc2c4056a, 0x83007a7a, 0x82c60a5d, 0x82c4092d, 0xc3006aab, 0x82c40a95,
    0x82c40b4a, 0x83004baa, 0xc2c60ad5, 0x82c4055a, 0x830128ba, 0x82c60a5b,
    0xc3007537, 0x82c4052b, 0x82c40693, 0x83015715, 0xc2c406aa, 0x82c60ad5,
    0x830035b5, 0x82c404b6, 0xc3008a5e, 0x82c40a4e, 0x82c40d26, 0x83006ea6,
    0xc2c40d52, 0x82c60daa, 0x8301466a, 0x82c6056d, 0xc2c404ae, 0x83003a9d,
    0x82c40a4d, 0x83007d2b, 0xc2c40b25, 0x82c40d52, 0x83015d54, 0x82c60b5a,
    0xc2c6055d, 0x8300355b, 0x82c4049b, 0x83007657, 0x82c40a4b, 0x82c40aa5,
    0x83006b65, 0x82c406d2, 0xc2c60ada, 0x830045b6, 0x82c60937, 0x82c40497,
    0xc3003697, 0x82c4064d, 0x82fe76aa, 0x82c60da5, 0xc2c405aa, 0x83005aec,
    0x82c60aae, 0x82c4092e, 0xc3003d2e, 0x82c40c96, 0x83018d45, 0x82c40d4a,
    0xc2c60d55, 0x83016595, 0x82c4056a, 0x82c60a6d, 0xc300455d, 0x82c4052d,
    0x82c40a95, 0x83013c95, 0xc2c40b4a, 0x83017b4a, 0x82c60ad5, 0x82c4055a,
    0xc3015a3a, 0x82c60a5b, 0x82c4052b, 0x83014a17, 0xc2c40693, 0x830096ab,
    0x82c406aa, 0x82c60ab5, 0xc30064f5, 0x82c404b6, 0x82c60a57, 0x82fe452e,
    0xc2c40d16, 0x82c60e93, 0x82fe3752, 0x82c60daa, 0xc30175aa, 0x82c6056d,
    0x82c404ae, 0x83015a1d, 0xc2c40a2d, 0x82c40d15, 0x83004da5, 0x82c40b52,
    0xc3009d6a, 0x82c60ada, 0x82c6055d, 0x8301629b, 0xc2c4045b, 0x82c40a2b,
    0x83005b2b, 0x82c40a95, 0xc2c40b52, 0x83012ab2, 0x82c60ad6, 0x83017556,
    0xc2c60537, 0x82c40457, 0x83005657, 0x82c4052b, 0xc2c40695, 0x83003795,
    0x82c405aa, 0x8300aab6, 0xc2c60a6d, 0x82c404ae, 0x83006a6e, 0x82c40a56,
    0xc2c40d2a, 0x83005eaa, 0x82c60d55, 0x82c405aa, 0xc3003b6a, 0x82c60a6d,
    0x830074bd, 0x82c404ab, 0xc2c40a8d, 0x83005d55, 0x82c40b2a, 0x82c60b55,
    0xc30045d5, 0x82c404da, 0x82c6095d, 0x83002557, 0xc2c4049b, 0x83006a97,
    0x82c4064b, 0x82c406a9, 0x83004baa, 0x82c606b5, 0x82c402ba, 0x83002ab6,
    0xc2c60937, 0x82fe652e, 0x82c40d16, 0x82c60e4b, 0xc2fe56d2, 0x82c60da9,
    0x82c605b5, 0x8300336d, 0xc2c402ae, 0x82c40a2e, 0x83002e2d, 0x82c40c95,
    0xc3006d55, 0x82c40b52, 0x82c60b69, 0x830045da, 0xc2c6055d, 0x82c4025d,
    0x83003a5b, 0x82c40a2b, 0xc3017a8b, 0x82c40a95, 0x82c40b4a, 0x83015b2a,
    0xc2c60ad5, 0x82c6055b, 0x830042b7, 0x82c40257, 0xc300952f, 0x82c4052b,
    0x82c40695, 0x830066d5, 0xc2c405aa, 0x82c60ab5, 0x8300456d, 0x82c404ae,
    0xc2c60a57, 0x82ff3456, 0x82c40d2a, 0x83017e8a, 0xc2c60d55, 0x82c405aa,
    0x83005ada, 0x82c6095d, 0xc2c404ae, 0x83004aab, 0x82c40a4d, 0x83008d2b,
    0xc2c40b29, 0x82c60b55, 0x83007575, 0x82c402da, 0xc2c6095d, 0x830054d7,
    0x82c4049b, 0x82c40a4b, 0xc3013a4b, 0x82c406a9, 0x83008ad9, 0x82c606b5,
    0xc2c402b6, 0x83015936, 0x82c60937, 0x82c40497, 0xc2fe4696, 0x82c40e4a,
    0x8300aea6, 0x82c60da9, 0xc2c605ad, 0x830162ad, 0x82c402ae, 0x82c4092e,
    0xc3005cad, 0x82c40c95, 0x82c40d4a, 0x83013d4a, 0xc2c60b69, 0x8300757a,
    0x82c6055b, 0x82c4025d, 0xc300595b, 0x82c4092b, 0x82c40a95, 0x83004d95,
    0xc2c40b4a, 0x82c60b55, 0x830026d5, 0x82c6055b, 0xc3006277, 0x82c40257,
    0x82c4052b, 0x82fe5aaa, 0xc2c60e95, 0x82c406aa, 0x83003baa, 0x82c60ab5,
    0x830084bd, 0x82c404ae, 0x82c60a57, 0x82fe554d, 0xc2c40d26, 0x82c60d95,
    0x83014655, 0x82c4056a, 0xc2c609ad, 0x8300255d, 0x82c404ae, 0x83006a5b,
    0xc2c40a4d, 0x82c40d25, 0x83005da9, 0x82c60b55, 0xc2c4056a, 0x83002ada,
    0x82c6095d, 0x830074bb, 0xc2c4049b, 0x82c40a4b, 0x83005b4b, 0x82c406a9,
    0xc2c40ad4, 0x83024bb5, 0x82c402b6, 0x82c6095b, 0xc3002537, 0x82c40497,
    0x82fe6656, 0x82c40e4a, 0xc2c60ea5, 0x830156a9, 0x82c605b5, 0x82c402b6,
    0xc30138ae, 0x82c4092e, 0x83017c8d, 0x82c40c95, 0xc2c40d4a, 0x83016d8a,
    0x82c60b69, 0x82c6056d, 0xc301425b, 0x82c4025d, 0x82c4092d, 0x83002d2b,
    0xc2c40a95, 0x83007d55, 0x82c40b4a, 0x82c60b55, 0xc3015555, 0x82c604db,
    0x82c4025b, 0x83013857, 0xc2c4052b, 0x83008a9b, 0x82c40695, 0x82c406aa,
    0xc3006aea, 0x82c60ab5, 0x82c404b6, 0x83004aae, 0xc2c60a57, 0x82c40527,
    0x82fe3726, 0x82c60d95, 0xc30076b5, 0x82c4056a, 0x82c609ad, 0x830054dd,
    0xc2c404ae, 0x82c40a4e, 0x83004d4d, 0x82c40d25, 0xc3008d59, 0x82c40b54,
    0x82c60d6a, 0x8301695a, 0xc2c6095b, 0x82c4049b, 0x83004a9b, 0x82c40a4b,
    0xc300ab27, 0x82c406a5, 0x82c406d4, 0x83026b75, 0xc2c402b6, 0x82c6095b,
    0x830054b7, 0x82c40497, 0xc2c4064b, 0x82fe374a, 0x82c60ea5, 0x830086d9,
    0xc2c605ad, 0x82c402b6, 0x8300596e, 0x82c4092e, 0xc2c40c96, 0x83004e95,
    0x82c40d4a, 0x82c60da5, 0xc3002755, 0x82c4056c, 0x83027abb, 0x82c4025d,
    0xc2c4092d, 0x83005cab, 0x82c40a95, 0x82c40b4a, 0xc3013b4a, 0x82c60b55,
    0x8300955d, 0x82c404ba, 0xc2c60a5b, 0x83005557, 0x82c4052b, 0x82c40a95,
    0xc3004b95, 0x82c406aa, 0x82c60ad5, 0x830026b5, 0xc2c404b6, 0x83006a6e,
    0x82c60a57, 0x82c40527, 0xc2fe56a6, 0x82c60d93, 0x82c405aa, 0x83003b6a,
    0xc2c6096d, 0x8300b4af, 0x82c404ae, 0x82c40a4d, 0xc3016d0d, 0x82c40d25,
    0x82c40d52, 0x83005dd4, 0xc2c60b6a, 0x82c6096d, 0x8300255b, 0x82c4049b,
    0xc3007a57, 0x82c40a4b, 0x82c40b25, 0x83015b25, 0xc2c406d4, 0x82c60ada,
    0x830138b6,
  ],
};


                               
               
                
              
                          
 

                            
               
                
              
                         
 

// Offsets that anchor the sexagenary cycle to the base year (1000): the cheongan
// (천간, length 10) and ganji (지지, length 12) wheels each start at a fixed
// position. Named so the gapja math reads as "cycle position + epoch offset"
// instead of bare numbers.
const GAPJA_OFFSET = {
  YEAR_CHEONGAN: 6,
  YEAR_GANJI: 0,
  MONTH_CHEONGAN: 3,
  MONTH_GANJI: 1,
  DAY_CHEONGAN: 4,
  DAY_GANJI: 2,
}         ;

class KoreanLunarCalendar {
          solarCalendar              ;
          lunarCalendar              ;

  // Memoized cumulative day counts from the base year. The month-search loops
  // call the *BeforeBaseYear helpers repeatedly with the same year, so caching
  // avoids re-summing ~1000 years on every lookup.
          cumulativeLunarYearDays = new Map                ();
          cumulativeSolarYearDays = new Map                ();

  constructor() {
    this.solarCalendar = { year: 0, month: 0, day: 0 };
    this.lunarCalendar = { year: 0, month: 0, day: 0, intercalation: false };

    // Default to today's solar date until an explicit date is set.
    const today = new Date();
    this.setSolarDate(
      today.getFullYear(),
      today.getMonth() + 1,
      today.getDate(),
    );
  }

          getLunarData(year        )         {
    return LUNAR_CALENDAR_DATA.KOREAN_LUNAR_DATA[
      year - LUNAR_CALENDAR_DATA.KOREAN_LUNAR_BASE_YEAR
    ];
  }

          getLunarIntercalationMonth(lunarData        )         {
    return (lunarData >> 12) & 0x000f;
  }

  // Total number of lunar days in the given year.
          getLunarYearDays(year        )         {
    return (this.getLunarData(year) >> 17) & 0x01ff;
  }

  // Number of days (29 or 30) in a specific lunar month.
          getLunarMonthDays(
    year        ,
    month        ,
    isIntercalation         ,
  )         {
    const lunarData = this.getLunarData(year);
    const isBigMonth =
      isIntercalation && this.getLunarIntercalationMonth(lunarData) === month
        ? ((lunarData >> 16) & 0x01) > 0
        : ((lunarData >> (12 - month)) & 0x01) > 0;
    return isBigMonth
      ? LUNAR_CALENDAR_DATA.LUNAR_BIG_MONTH_DAY
      : LUNAR_CALENDAR_DATA.LUNAR_SMALL_MONTH_DAY;
  }

          getLunarDaysBeforeBaseYear(year        )         {
    return this.accumulateYearDays(year, this.cumulativeLunarYearDays, (y) =>
      this.getLunarYearDays(y),
    );
  }

          getLunarDaysBeforeBaseMonth(
    year        ,
    month        ,
    isIntercalation         ,
  )         {
    let days = 0;
    if (year >= LUNAR_CALENDAR_DATA.KOREAN_LUNAR_BASE_YEAR && month > 0) {
      for (let baseMonth = 1; baseMonth < month + 1; baseMonth++) {
        days += this.getLunarMonthDays(year, baseMonth, false);
      }

      if (isIntercalation) {
        const intercalationMonth = this.getLunarIntercalationMonth(
          this.getLunarData(year),
        );
        if (intercalationMonth > 0 && intercalationMonth < month + 1) {
          days += this.getLunarMonthDays(year, intercalationMonth, true);
        }
      }
    }
    return days;
  }

          getLunarAbsDays(
    year        ,
    month        ,
    day        ,
    isIntercalation         ,
  )         {
    let days =
      this.getLunarDaysBeforeBaseYear(year - 1) +
      this.getLunarDaysBeforeBaseMonth(year, month - 1, true) +
      day;

    if (
      isIntercalation &&
      this.getLunarIntercalationMonth(this.getLunarData(year)) === month
    ) {
      days += this.getLunarMonthDays(year, month, false);
    }
    return days;
  }

          isSolarIntercalationYear(lunarData        )          {
    return ((lunarData >> 30) & 0x01) > 0;
  }

  // Total number of solar days (365 or 366) in the given year.
          getSolarYearDays(year        )         {
    return this.isSolarIntercalationYear(this.getLunarData(year))
      ? LUNAR_CALENDAR_DATA.SOLAR_BIG_YEAR_DAY
      : LUNAR_CALENDAR_DATA.SOLAR_SMALL_YEAR_DAY;
  }

  // Number of days in a specific solar month (February has 29 in a leap year).
          getSolarMonthDays(year        , month        )         {
    if (month === 2 && this.isSolarIntercalationYear(this.getLunarData(year))) {
      return LUNAR_CALENDAR_DATA.SOLAR_DAYS[12];
    }
    return LUNAR_CALENDAR_DATA.SOLAR_DAYS[month - 1];
  }

          getSolarDaysBeforeBaseYear(year        )         {
    return this.accumulateYearDays(year, this.cumulativeSolarYearDays, (y) =>
      this.getSolarYearDays(y),
    );
  }

  // Sum of per-year day counts from the base year through `year`, memoized.
  // Extends the previous year's cached sum when available (amortized O(1)),
  // otherwise sums from the base year once and caches the total.
          accumulateYearDays(
    year        ,
    cache                     ,
    perYear                       ,
  )         {
    const cached = cache.get(year);
    if (cached !== undefined) {
      return cached;
    }

    const baseYear = LUNAR_CALENDAR_DATA.KOREAN_LUNAR_BASE_YEAR;
    const previous = cache.get(year - 1);
    let days = 0;
    if (previous !== undefined && year > baseYear) {
      days = previous + perYear(year);
    } else {
      for (let y = baseYear; y < year + 1; y++) {
        days += perYear(y);
      }
    }

    cache.set(year, days);
    return days;
  }

          getSolarDaysBeforeBaseMonth(year        , month        )         {
    let days = 0;
    for (let baseMonth = 1; baseMonth < month + 1; baseMonth++) {
      days += this.getSolarMonthDays(year, baseMonth);
    }
    return days;
  }

          getSolarAbsDays(year        , month        , day        )         {
    return (
      this.getSolarDaysBeforeBaseYear(year - 1) +
      this.getSolarDaysBeforeBaseMonth(year, month - 1) +
      day -
      LUNAR_CALENDAR_DATA.SOLAR_LUNAR_DAY_DIFF
    );
  }

          setSolarDateByLunarDate(
    lunarYear        ,
    lunarMonth        ,
    lunarDay        ,
    isIntercalation         ,
  )       {
    const absDays = this.getLunarAbsDays(
      lunarYear,
      lunarMonth,
      lunarDay,
      isIntercalation,
    );
    const solarYear =
      absDays < this.getSolarAbsDays(lunarYear + 1, 1, 1)
        ? lunarYear
        : lunarYear + 1;
    let solarMonth = 0;
    let solarDay = 0;

    for (let month = 12; month > 0; month--) {
      const absDaysByMonth = this.getSolarAbsDays(solarYear, month, 1);
      if (absDays >= absDaysByMonth) {
        solarMonth = month;
        solarDay = absDays - absDaysByMonth + 1;
        break;
      }
    }

    this.solarCalendar = { year: solarYear, month: solarMonth, day: solarDay };
  }

          setLunarDateBySolarDate(
    solarYear        ,
    solarMonth        ,
    solarDay        ,
  )       {
    const absDays = this.getSolarAbsDays(solarYear, solarMonth, solarDay);
    const lunarYear =
      absDays >= this.getLunarAbsDays(solarYear, 1, 1, false)
        ? solarYear
        : solarYear - 1;
    let lunarMonth = 0;
    let lunarDay = 0;
    let isIntercalation = false;

    for (let month = 12; month > 0; month--) {
      const absDaysByMonth = this.getLunarAbsDays(lunarYear, month, 1, false);
      if (absDays >= absDaysByMonth) {
        lunarMonth = month;

        if (
          this.getLunarIntercalationMonth(this.getLunarData(lunarYear)) ===
          month
        ) {
          isIntercalation =
            absDays >= this.getLunarAbsDays(lunarYear, month, 1, true);
        }

        lunarDay =
          absDays -
          this.getLunarAbsDays(lunarYear, lunarMonth, 1, isIntercalation) +
          1;
        break;
      }
    }

    this.lunarCalendar = {
      year: lunarYear,
      month: lunarMonth,
      day: lunarDay,
      intercalation: isIntercalation,
    };
  }

          checkValidDate(
    isLunar         ,
    isIntercalation         ,
    year        ,
    month        ,
    day        ,
  )          {
    let isValid = false;
    // Reject non-integer / NaN inputs before they corrupt the bitfield math.
    if (
      !Number.isInteger(year) ||
      !Number.isInteger(month) ||
      !Number.isInteger(day)
    ) {
      return false;
    }
    const dateValue = year * 10000 + month * 100 + day;
    // 1582. 10. 5 ~ 1582. 10. 14 is not enable
    if (
      (isLunar
        ? LUNAR_CALENDAR_DATA.KOREAN_LUNAR_MIN_VALUE
        : LUNAR_CALENDAR_DATA.KOREAN_SOLAR_MIN_VALUE) <= dateValue &&
      (isLunar
        ? LUNAR_CALENDAR_DATA.KOREAN_LUNAR_MAX_VALUE
        : LUNAR_CALENDAR_DATA.KOREAN_SOLAR_MAX_VALUE) >= dateValue
    ) {
      if (month > 0 && month < 13 && day > 0) {
        // A leap-month request is only valid when this year's actual
        // intercalation month matches the requested month.
        if (
          isLunar &&
          isIntercalation &&
          this.getLunarIntercalationMonth(this.getLunarData(year)) !== month
        ) {
          return false;
        }
        const dayLimit = isLunar
          ? this.getLunarMonthDays(year, month, isIntercalation)
          : this.getSolarMonthDays(year, month);
        // 1582.10.5 ~ 1582.10.14 were skipped by the Gregorian reform; the
        // month still ends at day 31, so only those 10 days are rejected.
        if (!isLunar && year === 1582 && month === 10 && day > 4 && day < 15) {
          return false;
        }
        if (day <= dayLimit) {
          isValid = true;
        }
      }
    }
    return isValid;
  }

         setLunarDate(
    lunarYear        ,
    lunarMonth        ,
    lunarDay        ,
    isIntercalation         ,
  )          {
    let isValid = false;
    if (
      this.checkValidDate(
        true,
        isIntercalation,
        lunarYear,
        lunarMonth,
        lunarDay,
      )
    ) {
      this.lunarCalendar = {
        year: lunarYear,
        month: lunarMonth,
        day: lunarDay,
        intercalation:
          isIntercalation &&
          this.getLunarIntercalationMonth(this.getLunarData(lunarYear)) ===
            lunarMonth,
      };

      this.setSolarDateByLunarDate(
        lunarYear,
        lunarMonth,
        lunarDay,
        isIntercalation,
      );
      isValid = true;
    }
    return isValid;
  }

         setSolarDate(
    solarYear        ,
    solarMonth        ,
    solarDay        ,
  )          {
    let isValid = false;
    if (this.checkValidDate(false, false, solarYear, solarMonth, solarDay)) {
      this.solarCalendar = {
        year: solarYear,
        month: solarMonth,
        day: solarDay,
      };

      this.setLunarDateBySolarDate(solarYear, solarMonth, solarDay);
      isValid = true;
    }
    return isValid;
  }

  // Sexagenary-cycle indices for the current lunar date. Pure: returns a fresh
  // object instead of mutating instance state. When no valid date is set
  // (absDays <= 0) it returns the zero indices, preserving the historical
  // default of 갑자(甲子) for an unset converter.
          computeGapJa() {
    const lunar = this.lunarCalendar;
    const absDays = this.getLunarAbsDays(
      lunar.year,
      lunar.month,
      lunar.day,
      !!lunar.intercalation,
    );

    if (absDays <= 0) {
      return {
        cheongan: { year: 0, month: 0, day: 0 },
        ganji: { year: 0, month: 0, day: 0 },
      };
    }

    const baseYear = LUNAR_CALENDAR_DATA.KOREAN_LUNAR_BASE_YEAR;
    const cheonganLen = LUNAR_CALENDAR_DATA.KOREAN_CHEONGAN.length;
    const ganjiLen = LUNAR_CALENDAR_DATA.KOREAN_GANJI.length;
    const monthCount = lunar.month + 12 * (lunar.year - baseYear);

    return {
      cheongan: {
        year:
          (lunar.year + GAPJA_OFFSET.YEAR_CHEONGAN - baseYear) % cheonganLen,
        month: (monthCount + GAPJA_OFFSET.MONTH_CHEONGAN) % cheonganLen,
        day: (absDays + GAPJA_OFFSET.DAY_CHEONGAN) % cheonganLen,
      },
      ganji: {
        year: (lunar.year + GAPJA_OFFSET.YEAR_GANJI - baseYear) % ganjiLen,
        month: (monthCount + GAPJA_OFFSET.MONTH_GANJI) % ganjiLen,
        day: (absDays + GAPJA_OFFSET.DAY_GANJI) % ganjiLen,
      },
    };
  }

         getGapJaIndex() {
    return this.computeGapJa();
  }

         getGapja(isChinese          )            {
    const inx = this.getGapJaIndex();
    const cheongan = !isChinese
      ? LUNAR_CALENDAR_DATA.KOREAN_CHEONGAN
      : LUNAR_CALENDAR_DATA.CHINESE_CHEONGAN;
    const ganji = !isChinese
      ? LUNAR_CALENDAR_DATA.KOREAN_GANJI
      : LUNAR_CALENDAR_DATA.CHINESE_GANJI;
    const unit = !isChinese
      ? LUNAR_CALENDAR_DATA.KOREAN_GAPJA_UNIT
      : LUNAR_CALENDAR_DATA.CHINESE_GAPJA_UNIT;
    const intercalationStr = !isChinese
      ? `${LUNAR_CALENDAR_DATA.INTERCALATION_STR[0]}${LUNAR_CALENDAR_DATA.KOREAN_GAPJA_UNIT[1]}`
      : `${LUNAR_CALENDAR_DATA.INTERCALATION_STR[1]}${LUNAR_CALENDAR_DATA.CHINESE_GAPJA_UNIT[1]}`;

    return {
      year: `${cheongan[inx.cheongan.year]}${ganji[inx.ganji.year]}${unit[0]}`,
      month: `${cheongan[inx.cheongan.month]}${ganji[inx.ganji.month]}${unit[1]}`,
      day: `${cheongan[inx.cheongan.day]}${ganji[inx.ganji.day]}${unit[2]}`,
      intercalation: this.lunarCalendar.intercalation ? intercalationStr : "",
    };
  }

         getKoreanGapja()            {
    return this.getGapja();
  }

         getChineseGapja()            {
    return this.getGapja(true);
  }

         getLunarCalendar()               {
    return { ...this.lunarCalendar };
  }

         getSolarCalendar()               {
    return { ...this.solarCalendar };
  }
}


// shortcuts for easier to read formulas
const {PI, sin, cos, tan, asin, atan2: atan, acos, sqrt, abs, round, floor} = Math;
const rad = PI / 180;

// date/time constants and conversions

const dayMs = 1000 * 60 * 60 * 24;
const J1970 = 2440588;
const J2000 = 2451545;
const earthRadius = 6378.14; // equatorial radius in km, for the Moon's topocentric parallax

function fromJulian(j) {
    return new Date((j + 0.5 - J1970) * dayMs);
}
function toDays(date) {
    return date.valueOf() / dayMs - 0.5 + J1970 - J2000;
}

// ΔT = TT − UT in seconds (Espenak & Meeus polynomial fits, good ~1900–2150). The Meeus position
// series are defined in Terrestrial Time, but SunCalc's input Dates are UT — so the position math
// runs on days-since-J2000 shifted by deltaT, while sidereal time stays on UT. ~69 s today;
// negligible for the Sun (<0.001°), real for the Moon. d only needs ~month accuracy here (ΔT
// changes <1 s/yr), so the decimal year is derived arithmetically from d rather than from the Date.
function deltaT(d) {
    const y = 2000 + d / 365.2425;
    let t;
    if (y < 1920) { t = y - 1900; return -2.79 + t * (1.494119 + t * (-0.0598939 + t * (0.0061966 - t * 0.000197))); }
    if (y < 1941) { t = y - 1920; return 21.20 + t * (0.84493 + t * (-0.076100 + t * 0.0020936)); }
    if (y < 1961) { t = y - 1950; return 29.07 + t * (0.407 + t * (-1 / 233 + t / 2547)); }
    if (y < 1986) { t = y - 1975; return 45.45 + t * (1.067 + t * (-1 / 260 - t / 718)); }
    if (y < 2005) { t = y - 2000; return 63.86 + t * (0.3345 + t * (-0.060374 + t * (0.0017275 + t * (0.000651814 + t * 0.00002373599)))); }
    if (y < 2050) { t = y - 2000; return 62.92 + t * (0.32217 + t * 0.005589); }
    t = (y - 1820) / 100; return -20 + 32 * t * t - 0.5628 * (2150 - y);
}
function toDaysTT(d) {
    return d + deltaT(d) / 86400;
}

function sunCoords(d) {
    const t = d / 36525;
    const L0 = rad * (280.46646 + t * (36000.76983 + t * 0.0003032)); // 25.2 geometric mean longitude
    const M = rad * (357.52911 + t * (35999.05029 - t * 0.0001537)); // 25.3 mean anomaly
    const sinM = sin(M);
    const cosM = cos(M);
    const C = rad * ((1.914602 - t * (0.004817 + t * 0.000014)) * sinM + // equation of center
        (0.019993 - 0.000101 * t) * 2 * sinM * cosM + 0.000289 * sinM * (3 - 4 * sinM * sinM));
    const Om = rad * (125.04 - 1934.136 * t); // longitude of the ascending node
    const L = L0 + C - rad * (0.00569 + 0.00478 * sin(Om)); // apparent longitude (nutation + aberration)
    // 22.2 mean obliquity + 25.8 correction for apparent position
    const e = rad * (23.439291 - t * (0.0130042 + t * (0.00000016 - t * 0.000000504))) + rad * 0.00256 * cos(Om);

    return {
        ra: atan(cos(e) * sin(L), cos(L)), // 25.6
        dec: asin(sin(e) * sin(L)),        // 25.7
        lon: L
    };
}

// moon calculations, based on Meeus ch. 47 (truncated ELP-2000/82 series)

// Nutation in longitude (Δψ) and true obliquity of the ecliptic, both in degrees,
// from the abridged series of Meeus ch. 22 (sub-arcsecond, ample for our needs).
function nutationObliquity(t) {
    const om = rad * (125.04452 - 1934.136261 * t); // longitude of the Moon's ascending node
    const ls = rad * (280.4665 + 36000.7698 * t);   // mean longitude of the Sun
    const lm = rad * (218.3165 + 481267.8813 * t);  // mean longitude of the Moon
    const dpsi = (-17.20 * sin(om) - 1.32 * sin(2 * ls) - 0.23 * sin(2 * lm) + 0.21 * sin(2 * om)) / 3600;
    const deps = (9.20 * cos(om) + 0.57 * cos(2 * ls) + 0.10 * cos(2 * lm) - 0.09 * cos(2 * om)) / 3600;
    const eps0 = 23.439291 - t * (0.0130042 + t * (0.00000016 - t * 0.000000504)); // 22.2 mean obliquity
    return {dpsi, eps: rad * (eps0 + deps)};
}

// Meeus table 47.A — periodic terms for the Moon's longitude (Σl, ×1e-6 deg) and
// distance (Σr, ×1e-3 km). Flat rows of 6: D, M, M', F, Σl, Σr.
const moonLon = new Int32Array([
    0, 0, 1, 0, 6288774, -20905355,
    2, 0, -1, 0, 1274027, -3699111,
    2, 0, 0, 0, 658314, -2955968,
    0, 0, 2, 0, 213618, -569925,
    0, 1, 0, 0, -185116, 48888,
    0, 0, 0, 2, -114332, -3149,
    2, 0, -2, 0, 58793, 246158,
    2, -1, -1, 0, 57066, -152138,
    2, 0, 1, 0, 53322, -170733,
    2, -1, 0, 0, 45758, -204586,
    0, 1, -1, 0, -40923, -129620,
    1, 0, 0, 0, -34720, 108743,
    0, 1, 1, 0, -30383, 104755,
    2, 0, 0, -2, 15327, 10321,
    0, 0, 1, 2, -12528, 0,
    0, 0, 1, -2, 10980, 79661,
    4, 0, -1, 0, 10675, -34782,
    0, 0, 3, 0, 10034, -23210,
    4, 0, -2, 0, 8548, -21636,
    2, 1, -1, 0, -7888, 24208,
    2, 1, 0, 0, -6766, 30824,
    1, 0, -1, 0, -5163, -8379,
    1, 1, 0, 0, 4987, -16675,
    2, -1, 1, 0, 4036, -12831,
    2, 0, 2, 0, 3994, -10445,
    4, 0, 0, 0, 3861, -11650,
    2, 0, -3, 0, 3665, 14403,
    0, 1, -2, 0, -2689, -7003,
    2, 0, -1, 2, -2602, 0,
    2, -1, -2, 0, 2390, 10056,
    1, 0, 1, 0, -2348, 6322,
    2, -2, 0, 0, 2236, -9884,
    0, 1, 2, 0, -2120, 5751,
    0, 2, 0, 0, -2069, 0,
    2, -2, -1, 0, 2048, -4950,
    2, 0, 1, -2, -1773, 4130,
    2, 0, 0, 2, -1595, 0,
    4, -1, -1, 0, 1215, -3958,
    0, 0, 2, 2, -1110, 0,
    3, 0, -1, 0, -892, 3258,
    2, 1, 1, 0, -810, 2616,
    4, -1, -2, 0, 759, -1897,
    0, 2, -1, 0, -713, -2117,
    2, 2, -1, 0, -700, 2354,
    2, 1, -2, 0, 691, 0,
    2, -1, 0, -2, 596, 0,
    4, 0, 1, 0, 549, -1423,
    0, 0, 4, 0, 537, -1117,
    4, -1, 0, 0, 520, -1571,
    1, 0, -2, 0, -487, -1739,
    2, 1, 0, -2, -399, 0,
    0, 0, 2, -2, -381, -4421,
    1, 1, 1, 0, 351, 0,
    3, 0, -2, 0, -340, 0,
    4, 0, -3, 0, 330, 0,
    2, -1, 2, 0, 327, 0,
    0, 2, 1, 0, -323, 1165,
    1, 1, -1, 0, 299, 0,
    2, 0, 3, 0, 294, 0,
    2, 0, -1, -2, 0, 8752
]);

// Meeus table 47.B — periodic terms for the Moon's latitude (Σb, ×1e-6 deg).
// Flat rows of 5: D, M, M', F, Σb.
const moonLat = new Int32Array([
    0, 0, 0, 1, 5128122,
    0, 0, 1, 1, 280602,
    0, 0, 1, -1, 277693,
    2, 0, 0, -1, 173237,
    2, 0, -1, 1, 55413,
    2, 0, -1, -1, 46271,
    2, 0, 0, 1, 32573,
    0, 0, 2, 1, 17198,
    2, 0, 1, -1, 9266,
    0, 0, 2, -1, 8822,
    2, -1, 0, -1, 8216,
    2, 0, -2, -1, 4324,
    2, 0, 1, 1, 4200,
    2, 1, 0, -1, -3359,
    2, -1, -1, 1, 2463,
    2, -1, 0, 1, 2211,
    2, -1, -1, -1, 2065,
    0, 1, -1, -1, -1870,
    4, 0, -1, -1, 1828,
    0, 1, 0, 1, -1794,
    0, 0, 0, 3, -1749,
    0, 1, -1, 1, -1565,
    1, 0, 0, 1, -1491,
    0, 1, 1, 1, -1475,
    0, 1, 1, -1, -1410,
    0, 1, 0, -1, -1344,
    1, 0, 0, -1, -1335,
    0, 0, 3, 1, 1107,
    4, 0, 0, -1, 1021,
    4, 0, -1, 1, 833,
    0, 0, 1, -3, 777,
    4, 0, -2, 1, 671,
    2, 0, 0, -3, 607,
    2, 0, 2, -1, 596,
    2, -1, 1, -1, 491,
    2, 0, -2, 1, -451,
    0, 0, 3, -1, 439,
    2, 0, 2, 1, 422,
    2, 0, -3, -1, 421,
    2, 1, -1, 1, -366,
    2, 1, 0, 1, -351,
    4, 0, 0, 1, 331,
    2, -1, 1, 1, 315,
    2, -2, 0, -1, 302,
    0, 0, 1, 3, -283,
    2, 1, 1, -1, -229,
    1, 1, 0, -1, 223,
    1, 1, 0, 1, 223,
    0, 1, -2, -1, -220,
    2, 1, -1, -1, -220,
    1, 0, 1, 1, -185,
    2, -1, -2, -1, 181,
    0, 1, 2, 1, -177,
    4, 0, -2, -1, 176,
    4, -1, -1, -1, 166,
    1, 0, 1, -1, -164,
    4, 0, 1, -1, 132,
    1, 0, -1, -1, -119,
    4, -1, 0, -1, 115,
    2, -2, 0, 1, 107
]);

// geocentric apparent equatorial coordinates of the Moon, Meeus ch. 47. d = days since J2000 (TT).
function moonCoords(d) {
    const t = d / 36525;

    // fundamental arguments (degrees), 47.1–47.6
    const Lp = 218.3164477 + t * (481267.88123421 + t * (-0.0015786 + t * (1 / 538841 - t / 65194000)));
    const D = 297.8501921 + t * (445267.1114034 + t * (-0.0018819 + t * (1 / 545868 - t / 113065000)));
    const M = 357.5291092 + t * (35999.0502909 + t * (-0.0001536 + t / 24490000));
    const Mp = 134.9633964 + t * (477198.8675055 + t * (0.0087414 + t * (1 / 69699 - t / 14712000)));
    const F = 93.2720950 + t * (483202.0175233 + t * (-0.0036539 + t * (-1 / 3526000 + t / 863310000)));
    const A1 = 119.75 + 131.849 * t;
    const A2 = 53.09 + 479264.290 * t;
    const A3 = 313.45 + 481266.484 * t;
    const E = 1 - t * (0.002516 + t * 0.0000074); // eccentricity factor for solar-anomaly terms

    const Dr = rad * D, Mr = rad * M, Mpr = rad * Mp, Fr = rad * F;
    let sl = 0, sr = 0, sb = 0;
    for (let i = 0; i < moonLon.length; i += 6) {
        const m = moonLon[i + 1];
        const arg = moonLon[i] * Dr + m * Mr + moonLon[i + 2] * Mpr + moonLon[i + 3] * Fr;
        const f = m === 1 || m === -1 ? E : m === 2 || m === -2 ? E * E : 1;
        sl += moonLon[i + 4] * f * sin(arg);
        sr += moonLon[i + 5] * f * cos(arg);
    }
    for (let i = 0; i < moonLat.length; i += 5) {
        const m = moonLat[i + 1];
        const arg = moonLat[i] * Dr + m * Mr + moonLat[i + 2] * Mpr + moonLat[i + 3] * Fr;
        const f = m === 1 || m === -1 ? E : m === 2 || m === -2 ? E * E : 1;
        sb += moonLat[i + 4] * f * sin(arg);
    }

    // additive terms (Venus, Jupiter and flattening of the Earth), 47 p.342
    const A1r = rad * A1, Lpr = rad * Lp;
    sl += 3958 * sin(A1r) + 1962 * sin(Lpr - Fr) + 318 * sin(rad * A2);
    sb += -2235 * sin(Lpr) + 382 * sin(rad * A3) + 175 * sin(A1r - Fr) + 175 * sin(A1r + Fr) +
        127 * sin(Lpr - Mpr) - 115 * sin(Lpr + Mpr);

    const {dpsi, eps} = nutationObliquity(t);
    const l = rad * (Lp + sl / 1e6 + dpsi); // apparent ecliptic longitude
    const b = rad * (sb / 1e6);             // ecliptic latitude

    return {
        ra: atan(sin(l) * cos(eps) - tan(b) * sin(eps), cos(l)),  // 13.3
        dec: asin(sin(b) * cos(eps) + cos(b) * sin(eps) * sin(l)), // 13.4
        dist: 385000.56 + sr / 1000, // distance to the Moon in km
        lon: l
    };
}

// moon illumination parameters, Meeus ch. 48 (and idlastro's mphase.pro)
function getMoonIllumination(date = new Date()) {
    const d = toDaysTT(toDays(date));
    const s = sunCoords(d);
    const m = moonCoords(d);
    const sdist = 149598000; // distance from Earth to Sun in km
    const phi = acos(sin(s.dec) * sin(m.dec) + cos(s.dec) * cos(m.dec) * cos(s.ra - m.ra));
    const inc = atan(sdist * sin(phi), m.dist - sdist * cos(phi));
    const angle = atan(cos(s.dec) * sin(s.ra - m.ra), sin(s.dec) * cos(m.dec) -
        cos(s.dec) * sin(m.dec) * cos(s.ra - m.ra));

    // elongation in ecliptic longitude, which defines the named phases (Meeus ch. 49, USNO); the RA
    // difference behind `angle` crosses 0/180° hours off conjunction/opposition near the nodes
    const phase = (((m.lon - s.lon) / (2 * PI)) % 1 + 1) % 1;
    const waxing = phase < 0.5;

    return {
        // illuminated fraction, 0 (new) → 1 (full); reaches the exact extrema only at perfect
        // syzygy (eclipses), so a "full" moon typically peaks a hair under 1 — this is correct
        fraction: (1 + cos(inc)) / 2,
        // phase, 0 → 1: 0 new, 0.25 first quarter, 0.5 full, 0.75 last quarter (waxing for phase < 0.5)
        phase,
        // position angle of the bright limb, degrees (v2: all angles emitted in degrees) — subtract
        // getMoonPosition().parallacticAngle, also degrees, to get the zenith-relative tilt
        angle: angle / rad,
        waxing // true while the Moon is waxing (new → full), false while waning (full → new)
    };
}




const lunarConverter = new KoreanLunarCalendar();
const stems = '갑을병정무기경신임계'.split(''), branches = '자축인묘진사오미신유술해'.split('');
const mod = (x,n) => ((x%n)+n)%n;
function validDate(date){return date instanceof Date && Number.isFinite(date.getTime());}
function lunarFor(date){
  if(!validDate(date)||date.getUTCFullYear()<1900||date.getUTCFullYear()>2050)return null;
  if(!lunarConverter.setSolarDate(date.getUTCFullYear(),date.getUTCMonth()+1,date.getUTCDate()))return null;
  return lunarConverter.getLunarCalendar();
}
function moonAt(instant){
  if(!validDate(instant)||instant.getUTCFullYear()<1900||instant.getUTCFullYear()>2100)return null;
  const moon=getMoonIllumination(instant),index=Math.round(moon.phase*8)%8;
  const emojis=['🌑','🌒','🌓','🌔','🌕','🌖','🌗','🌘'];
  const labels=['삭 무렵','초승달','상현달 무렵','차오르는 달','보름달 무렵','기우는 달','하현달 무렵','그믐달'];
  return {phase:moon.phase,fraction:moon.fraction,emoji:emojis[index],label:labels[index]};
}
function moonFor(date){return validDate(date)?moonAt(new Date(Date.UTC(date.getUTCFullYear(),date.getUTCMonth(),date.getUTCDate(),3))):null;}
function pillarsAt(instant,events){
  if(!validDate(instant)||!Array.isArray(events)||events.length!==24)return null;
  const kst=new Date(instant.getTime()+9*3600000),year=kst.getUTCFullYear();
  if(year<1900||year>2100||events.some(e=>!Number.isFinite(e.milliseconds)||!Number.isInteger(e.termIndex)))return null;
  if(new Set(events.map(e=>e.termIndex)).size!==24)return null;
  const spring=events.find(e=>e.termIndex===21),solarYear=year-(instant.getTime()<spring.milliseconds?1:0);
  const jie=events.filter(e=>e.termIndex%2===1&&e.milliseconds<=instant.getTime()).sort((a,b)=>b.milliseconds-a.milliseconds)[0];
  const monthIndex=jie?mod(jie.termIndex-21,24)/2:10;
  const yearStem=mod(solarYear-4,10),yearBranch=mod(solarYear-4,12);
  const monthStem=mod((yearStem%5)*2+2+monthIndex,10),monthBranch=mod(monthIndex+2,12);
  const epochDay=Math.floor(Date.UTC(year,kst.getUTCMonth(),kst.getUTCDate())/86400000);
  const dayIndex=mod(epochDay-Math.floor(Date.UTC(2000,0,7)/86400000),60);
  return {year:stems[yearStem]+branches[yearBranch]+'년',month:stems[monthStem]+branches[monthBranch]+'월',day:stems[dayIndex%10]+branches[dayIndex%12]+'일'};
}
return {lunarFor,moonFor,moonAt,pillarsAt};
});
