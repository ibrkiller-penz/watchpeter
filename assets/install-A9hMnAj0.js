import{s as L}from"./pwa-CxqqUTio.js";L();const B="https://unpkg.com/esp-web-tools@10.1.1/dist/web/install-button.js?module",f="COM7",O=`esptool --chip esp32c6 -p ${f} flash-id`,W=`esptool --chip esp32c6 -p ${f} -b 460800 read-flash 0 ALL xiaozhi_backup.bin`,R="certutil -hashfile xiaozhi_backup.bin SHA256",D=`esptool --chip esp32c6 -p ${f} -b 460800 write-flash 0x0 xiaozhi_backup.bin`,i=n=>n.replace(/[&<>"']/g,r=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[r]);try{const n=localStorage.getItem("wrist-sim.theme");(n==="light"||n==="dark")&&(document.documentElement.dataset.theme=n)}catch{}const b=(n,r)=>`
  <div class="inst-code">
    <pre><code>${i(n)}</code></pre>
    <button type="button" class="inst-btn inst-copy" data-copy="${i(n)}" aria-label="${i(r)} 명령 복사">복사</button>
  </div>`,g=document.getElementById("install-root");if(g){const n="serial"in navigator,r=globalThis.isSecureContext;g.innerHTML=`
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
      <p>처음 설치하기 전에 지금 들어 있는 펌웨어(샤오즈)를 통째로 백업합니다. 되돌릴 수 있어야 합니다. Python 3.12 에서 <code>pip install esptool</code> 후, 포트(${f})는 장치 관리자에서 확인해 바꿉니다.</p>
      <ol class="inst-steps">
        <li>칩·플래시 확인 (실물: ESP32-C6, 16MB) ${b(O,"플래시 확인")}</li>
        <li>전체 백업 (<code>ALL</code> = 용량 자동 감지, 16MB 약 90초) ${b(W,"백업")}</li>
        <li>해시 기록 (두 번 받아 같은지 비교하면 더 안전) ${b(R,"해시")}</li>
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
          <li>시계를 연결하고(필요하면 BOOT 를 누른 채 전원) 전체 이미지를 0x0 에 씁니다. esptool v5 는 쓰고 나서 자동으로 검증합니다. ${b(D,"복원")}</li>
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

    <section class="inst-card" aria-labelledby="inst-s7">
      <h2 id="inst-s7"><span class="inst-n">7</span>PC 바로 가기 키 설정</h2>
      <p>시계 <strong>실행 모드 1쪽</strong> 타일은 <code>Ctrl+Alt+1~6</code> 을 보냅니다(1 Claude · 2 카카오톡 · 3 크롬 · 4 파워포인트 · 5 엑셀 · 6 한글). 수업용 PC 마다 한 번, 이 키로 앱이 열리도록 바로 가기를 만듭니다. 작업표시줄 순서·한/영 상태와 상관없이 동작합니다.</p>
      <ol class="inst-steps">
        <li><a href="./pc-setup/wrist-shortcuts.ps1" download="wrist-shortcuts.ps1">wrist-shortcuts.ps1 내려받기</a> (PowerShell 스크립트, 관리자 권한 필요 없음 — 내 시작 메뉴 <code>손목 컨트롤러</code> 폴더에 바로 가기 6개를 만듭니다)</li>
        <li>내려받은 파일을 <strong>오른쪽 클릭 → PowerShell 에서 실행</strong>. 실행이 막히면 내려받은 폴더에서 PowerShell 을 열고 아래 한 줄을 실행합니다. ${b("powershell -ExecutionPolicy Bypass -File .wrist-shortcuts.ps1","바로 가기 스크립트")}</li>
        <li>창에 <code>만듦</code> / <code>건너뜀</code> 이 앱마다 표시됩니다. 건너뛴 앱은 시작 메뉴에서 찾지 못한 것입니다(설치 후 다시 실행하면 됩니다. 다시 실행하면 덮어씁니다).</li>
        <li>실행 후 바로 가기 키가 안 먹으면 <strong>로그아웃 후 다시 로그인</strong>합니다.</li>
      </ol>
      <p class="inst-sub">타일을 길게 누르면 크롬·파워포인트·엑셀은 실행 창(Win+R)으로도 열 수 있습니다. macOS 는 이 설정 없이 Spotlight 로 엽니다.</p>
    </section>

    <p class="inst-foot">이 페이지의 설치 버튼은 사용자가 직접 누릅니다. 개발 중 자동으로 시계에 올리지 않습니다.</p>
  </main>`;const a=s=>g.querySelector(`[data-ref="${s}"]`),v=a("backup"),E=a("activate"),S=a("espBtn"),P=a("gate"),p=a("versions"),k=a("oldWarn");let o=[],d=null,w="loading";const c=()=>{const s=v.checked&&!!d&&n;E.disabled=!s;let t="";n?v.checked?d?d.example?t=`v${d.version} 은(는) 예시라 설치 파일이 없습니다 — 눌러도 매니페스트를 찾지 못해 아무것도 쓰지 않습니다.`:w==="error"&&(t="설치 도구(ESP Web Tools)를 불러오지 못했습니다. 인터넷 연결을 확인하세요."):t="설치할 버전을 고르세요.":t="2단계 백업 확인 체크를 켜면 설치 버튼이 활성화됩니다.":t="이 브라우저에서는 설치할 수 없습니다(데스크톱 Chrome·Edge 필요).",P.textContent=t};S.addEventListener("click",s=>{E.disabled&&(s.stopImmediatePropagation(),s.preventDefault())},!0),v.addEventListener("change",c);const $=s=>{d=s,S.setAttribute("manifest",s.manifest),k.hidden=o.length===0||s===o[0];for(const t of p.querySelectorAll('input[type="radio"]'))t.checked=t.value===s.version;c()},_=()=>{if(o.length===0){p.innerHTML='<p class="inst-sub">설치할 수 있는 버전이 없습니다.</p>';return}p.innerHTML=o.map((s,t)=>`
        <label class="inst-version">
          <input type="radio" name="inst-version" value="${i(s.version)}" />
          <span class="inst-version__main">
            <span class="inst-version__name">v${i(s.version)}</span>
            ${t===0?'<span class="inst-badge">최신 · 권장</span>':""}
            ${s.example?'<span class="inst-badge inst-badge--example">예시 · 파일 없음</span>':""}
            <span class="inst-version__date">${s.date?i(s.date):"날짜 없음"}</span>
          </span>
          <span class="inst-version__sub">${s.summary?i(s.summary):""}${s.notes?` · <a href="${i(s.notes)}" target="_blank" rel="noopener">변경 내역</a>`:" · 변경 내역(릴리스 후 연결)"}</span>
        </label>`).join(""),p.querySelectorAll('input[type="radio"]').forEach(s=>s.addEventListener("change",()=>{const t=o.find(e=>e.version===s.value);t&&$(t)})),$(o[0])};fetch("firmware/manifests.json",{cache:"no-cache"}).then(s=>{if(!s.ok)throw new Error(`HTTP ${s.status}`);return s.json()}).then(s=>{o=Array.isArray(s.versions)?s.versions:[],a("exampleNotice").hidden=!(s.example||o.some(t=>t.example)),_()}).catch(s=>{p.innerHTML=`<p class="inst-sub">버전 목록(firmware/manifests.json)을 불러오지 못했습니다: ${i(s instanceof Error?s.message:String(s))}</p>`,c()});const M=a("setTime"),y=a("timeMsg");if(M.addEventListener("click",async()=>{var t;const s=navigator.serial;if(s)try{const e=await s.requestPort();await e.open({baudRate:115200}),await((t=e.setSignals)==null?void 0:t.call(e,{dataTerminalReady:!1,requestToSend:!1}).catch(()=>{}));const u=async()=>{const h=Date.now(),A=-new Date().getTimezoneOffset(),T=`t ${Math.floor(h/1e3)} ${A}
`,x=e.writable.getWriter();return await x.write(new TextEncoder().encode(T)),x.releaseLock(),T.trim()};await new Promise(h=>setTimeout(h,300));const m=await u();y.textContent=`보냄: ${m} — 2초 뒤 한 번 더`,await new Promise(h=>setTimeout(h,2e3));const l=await u();await e.close();const C=new Date;y.textContent=`완료: ${l} (${C.toLocaleString()} · UTC${C.getTimezoneOffset()<=0?"+":"-"}${Math.abs(C.getTimezoneOffset()/60)})`}catch(e){y.textContent=`실패: ${e instanceof Error?e.message:String(e)} (다른 프로그램이 포트를 쓰고 있으면 닫으세요)`}}),g.querySelectorAll(".inst-copy").forEach(s=>s.addEventListener("click",async()=>{var e;const t=s.dataset.copy??"";try{await navigator.clipboard.writeText(t),s.textContent="복사됨"}catch{const u=(e=s.parentElement)==null?void 0:e.querySelector("code");if(u){const m=document.createRange();m.selectNodeContents(u);const l=getSelection();l==null||l.removeAllRanges(),l==null||l.addRange(m)}s.textContent="선택됨 — Ctrl+C"}setTimeout(()=>s.textContent="복사",1600)})),n){const s=document.createElement("script");s.type="module",s.src=B,s.onload=()=>{w="ok",c()},s.onerror=()=>{w="error",c()},document.head.append(s)}c()}
