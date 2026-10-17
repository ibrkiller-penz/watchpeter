import{s as A}from"./pwa-CxqqUTio.js";A();const B="https://unpkg.com/esp-web-tools@10.1.1/dist/web/install-button.js?module",g="COM7",O=`esptool --chip esp32c6 -p ${g} flash-id`,W=`esptool --chip esp32c6 -p ${g} -b 460800 read-flash 0 ALL xiaozhi_backup.bin`,R="certutil -hashfile xiaozhi_backup.bin SHA256",D=`esptool --chip esp32c6 -p ${g} -b 460800 write-flash 0x0 xiaozhi_backup.bin`,i=n=>n.replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r]);try{const n=localStorage.getItem("wrist-sim.theme");(n==="light"||n==="dark")&&(document.documentElement.dataset.theme=n)}catch{}const h=(n,r)=>`
  <div class="inst-code">
    <pre><code>${i(n)}</code></pre>
    <button type="button" class="inst-btn inst-copy" data-copy="${i(n)}" aria-label="${i(r)} 명령 복사">복사</button>
  </div>`,f=document.getElementById("install-root");if(f){const n="serial"in navigator,r=globalThis.isSecureContext;f.innerHTML=`
  <main class="inst-main">
    <p class="inst-back"><a href="./index.html">← 시뮬레이터로</a></p>
    <h1 class="inst-title">시계에 설치</h1>
    <p class="inst-lead">Waveshare ESP32-C6 2.06 AMOLED 시계에 손목 컨트롤러 펌웨어를 브라우저에서 USB 로 바로 설치합니다(ESP Web Tools). PC 에 프로그램을 설치하지 않아도 됩니다.</p>

    ${n?`<p class="inst-ok">Chrome·Edge 확인됨 (Web Serial 사용 가능)${r?"":" · 단, 보안 연결(https)이 아니라 설치가 막힙니다"}</p>`:'<div class="inst-notice" role="alert">이 페이지는 <strong>데스크톱 Chrome 또는 Edge</strong>에서만 설치할 수 있습니다(Web Serial 필요). Safari·Firefox·모바일은 지원하지 않습니다.</div>'}
    <div class="inst-notice inst-notice--example" data-ref="exampleNotice" hidden>
      <strong>아직 실제 릴리스가 없습니다.</strong> 아래 버전 목록은 예시이며 설치 파일(.bin)이 없습니다. 펌웨어 2단계와 배포 파이프라인이 끝나면 CI 가 이 목록을 채웁니다.
    </div>

    <section class="inst-card" aria-labelledby="inst-s1">
      <h2 id="inst-s1"><span class="inst-n">1</span>시계 연결</h2>
      <p>USB-C <strong>데이터</strong> 케이블로 시계를 PC 에 연결합니다(충전 전용 케이블은 인식되지 않습니다).</p>
      <p class="inst-sub">인식되지 않으면: BOOT 버튼을 누른 채 전원을 켜서 다운로드 모드로 들어간 뒤 다시 시도합니다(Waveshare 위키 기준 — 실물 확인 후 문구 확정).</p>
    </section>

    <section class="inst-card" aria-labelledby="inst-s2">
      <h2 id="inst-s2"><span class="inst-n">2</span>원래 펌웨어 백업</h2>
      <p>처음 설치하기 전에 지금 들어 있는 펌웨어(샤오즈)를 통째로 백업합니다. 되돌릴 수 있어야 합니다. Python 3.12 에서 <code>pip install esptool</code> 후, 포트(${g})는 장치 관리자에서 확인해 바꿉니다.</p>
      <ol class="inst-steps">
        <li>칩·플래시 확인 (실물: ESP32-C6, 16MB) ${h(O,"플래시 확인")}</li>
        <li>전체 백업 (<code>ALL</code> = 용량 자동 감지, 16MB 약 90초) ${h(W,"백업")}</li>
        <li>해시 기록 (두 번 받아 같은지 비교하면 더 안전) ${h(R,"해시")}</li>
      </ol>
      <label class="inst-checkrow">
        <input type="checkbox" data-ref="backup" />
        <span>원래 펌웨어(샤오즈)를 백업했습니다. 또는 이미 손목 컨트롤러 펌웨어가 설치되어 있습니다.</span>
      </label>
    </section>

    <section class="inst-card" aria-labelledby="inst-s3">
      <h2 id="inst-s3"><span class="inst-n">3</span>버전 선택</h2>
      <div class="inst-versions" role="radiogroup" aria-label="펌웨어 버전" data-ref="versions"><p class="inst-sub">버전 목록을 불러오는 중…</p></div>
      <div class="inst-notice" data-ref="oldWarn" hidden>이전 버전입니다. 설정이 초기화되고 PC 와 다시 페어링해야 할 수 있습니다.</div>
    </section>

    <section class="inst-card" aria-labelledby="inst-s4">
      <h2 id="inst-s4"><span class="inst-n">4</span>설치</h2>
      <p class="inst-sub">설치 대화상자에서 "장치 지우기(Erase)"를 고르면 설정·페어링이 초기화되어 PC 에서 다시 페어링해야 합니다. 샤오즈나 공장 펌웨어에서 처음 넘어올 때는 지우기를 고르세요.</p>
      <div class="inst-install">
        <esp-web-install-button data-ref="espBtn">
          <button slot="activate" type="button" class="inst-installbtn" data-ref="activate" disabled>시계에 설치</button>
          <span slot="unsupported" class="inst-notice">이 브라우저는 지원하지 않습니다. 데스크톱 Chrome 또는 Edge로 열어 주세요.</span>
          <span slot="not-allowed" class="inst-notice">보안 연결(https)에서만 설치할 수 있습니다.</span>
        </esp-web-install-button>
        <span class="inst-sub">설치 중에는 USB를 뽑지 마세요. 약 1분 걸립니다.</span>
      </div>
      <p class="inst-gate" data-ref="gate" aria-live="polite"></p>
    </section>

    <section class="inst-card">
      <details>
        <summary><span class="inst-n">5</span>원래 펌웨어(샤오즈)로 되돌리기</summary>
        <ol class="inst-steps">
          <li>2단계에서 받은 백업 파일 <code>xiaozhi_backup.bin</code> 위치를 확인하고, 그 폴더에서 명령 창을 엽니다.</li>
          <li>시계를 연결하고(필요하면 BOOT 를 누른 채 전원) 전체 이미지를 0x0 에 씁니다. esptool v5 는 쓰고 나서 자동으로 검증합니다. ${h(D,"복원")}</li>
          <li>전원을 다시 켭니다. 자세한 방법: 저장소 README 의 '원래 펌웨어 복원'.</li>
        </ol>
        <p class="inst-sub">ESP Web Tools 는 내 PC 의 파일을 직접 올리지 못해서 복원은 esptool 명령으로 합니다. 백업이 없으면 Waveshare 저장소 Release 의 공장 펌웨어로 복원할 수 있습니다(같은 명령, 파일만 바꿈).</p>
      </details>
    </section>

    <section class="inst-card" aria-labelledby="inst-s6">
      <h2 id="inst-s6"><span class="inst-n">6</span>시계 시간 맞추기</h2>
      <p>시계 모드의 시각은 보드 RTC(PCF85063A)에 저장됩니다(전원을 꺼도 유지). 처음 한 번, 또는 배터리를 뺀 뒤에 이 PC 의 시각으로 맞춥니다.</p>
      <p class="inst-sub">USB 로 연결한 채 버튼을 누르고 시계 포트를 고르면 <code>t &lt;유닉스 초&gt; &lt;시간대 분&gt;</code> 명령을 보냅니다(직렬 명령, README '시계 안 조작'). 포트를 열 때 시계가 다시 켜질 수 있어 2초 뒤 한 번 더 보냅니다.</p>
      <div class="inst-install">
        <button type="button" class="inst-installbtn" data-ref="setTime" ${n?"":"disabled"}>시계 시간 맞추기</button>
        <span class="inst-sub" data-ref="timeMsg" aria-live="polite"></span>
      </div>
    </section>

    <p class="inst-foot">이 페이지의 설치 버튼은 사용자가 직접 누릅니다. 개발 중 자동으로 시계에 올리지 않습니다.</p>
  </main>`;const a=s=>f.querySelector(`[data-ref="${s}"]`),v=a("backup"),C=a("activate"),w=a("espBtn"),k=a("gate"),p=a("versions"),P=a("oldWarn");let o=[],d=null,y="loading";const c=()=>{const s=v.checked&&!!d&&n;C.disabled=!s;let e="";n?v.checked?d?d.example?e=`v${d.version} 은(는) 예시라 설치 파일이 없습니다 — 눌러도 매니페스트를 찾지 못해 아무것도 쓰지 않습니다.`:y==="error"&&(e="설치 도구(ESP Web Tools)를 불러오지 못했습니다. 인터넷 연결을 확인하세요."):e="설치할 버전을 고르세요.":e="2단계 백업 확인 체크를 켜면 설치 버튼이 활성화됩니다.":e="이 브라우저에서는 설치할 수 없습니다(데스크톱 Chrome·Edge 필요).",k.textContent=e};w.addEventListener("click",s=>{C.disabled&&(s.stopImmediatePropagation(),s.preventDefault())},!0),v.addEventListener("change",c);const S=s=>{d=s,w.setAttribute("manifest",s.manifest),P.hidden=o.length===0||s===o[0];for(const e of p.querySelectorAll('input[type="radio"]'))e.checked=e.value===s.version;c()},_=()=>{if(o.length===0){p.innerHTML='<p class="inst-sub">설치할 수 있는 버전이 없습니다.</p>';return}p.innerHTML=o.map((s,e)=>`
        <label class="inst-version">
          <input type="radio" name="inst-version" value="${i(s.version)}" />
          <span class="inst-version__main">
            <span class="inst-version__name">v${i(s.version)}</span>
            ${e===0?'<span class="inst-badge">최신 · 권장</span>':""}
            ${s.example?'<span class="inst-badge inst-badge--example">예시 · 파일 없음</span>':""}
            <span class="inst-version__date">${s.date?i(s.date):"날짜 없음"}</span>
          </span>
          <span class="inst-version__sub">${s.summary?i(s.summary):""}${s.notes?` · <a href="${i(s.notes)}" target="_blank" rel="noopener">변경 내역</a>`:" · 변경 내역(릴리스 후 연결)"}</span>
        </label>`).join(""),p.querySelectorAll('input[type="radio"]').forEach(s=>s.addEventListener("change",()=>{const e=o.find(t=>t.version===s.value);e&&S(e)})),S(o[0])};fetch("firmware/manifests.json",{cache:"no-cache"}).then(s=>{if(!s.ok)throw new Error(`HTTP ${s.status}`);return s.json()}).then(s=>{o=Array.isArray(s.versions)?s.versions:[],a("exampleNotice").hidden=!(s.example||o.some(e=>e.example)),_()}).catch(s=>{p.innerHTML=`<p class="inst-sub">버전 목록(firmware/manifests.json)을 불러오지 못했습니다: ${i(s instanceof Error?s.message:String(s))}</p>`,c()});const M=a("setTime"),E=a("timeMsg");if(M.addEventListener("click",async()=>{var e;const s=navigator.serial;if(s)try{const t=await s.requestPort();await t.open({baudRate:115200}),await((e=t.setSignals)==null?void 0:e.call(t,{dataTerminalReady:!1,requestToSend:!1}).catch(()=>{}));const u=async()=>{const m=Date.now(),L=-new Date().getTimezoneOffset(),T=`t ${Math.floor(m/1e3)} ${L}
`,x=t.writable.getWriter();return await x.write(new TextEncoder().encode(T)),x.releaseLock(),T.trim()};await new Promise(m=>setTimeout(m,300));const b=await u();E.textContent=`보냄: ${b} — 2초 뒤 한 번 더`,await new Promise(m=>setTimeout(m,2e3));const l=await u();await t.close();const $=new Date;E.textContent=`완료: ${l} (${$.toLocaleString()} · UTC${$.getTimezoneOffset()<=0?"+":"-"}${Math.abs($.getTimezoneOffset()/60)})`}catch(t){E.textContent=`실패: ${t instanceof Error?t.message:String(t)} (다른 프로그램이 포트를 쓰고 있으면 닫으세요)`}}),f.querySelectorAll(".inst-copy").forEach(s=>s.addEventListener("click",async()=>{var t;const e=s.dataset.copy??"";try{await navigator.clipboard.writeText(e),s.textContent="복사됨"}catch{const u=(t=s.parentElement)==null?void 0:t.querySelector("code");if(u){const b=document.createRange();b.selectNodeContents(u);const l=getSelection();l==null||l.removeAllRanges(),l==null||l.addRange(b)}s.textContent="선택됨 — Ctrl+C"}setTimeout(()=>s.textContent="복사",1600)})),n){const s=document.createElement("script");s.type="module",s.src=B,s.onload=()=>{y="ok",c()},s.onerror=()=>{y="error",c()},document.head.append(s)}c()}
