import{s as i}from"./pwa-CxqqUTio.js";/* empty css                */i();const r="powershell -ExecutionPolicy Bypass -File .\\wrist-shortcuts.ps1",n=t=>t.replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e]);try{const t=localStorage.getItem("wrist-sim.theme");(t==="light"||t==="dark")&&(document.documentElement.dataset.theme=t)}catch{}const p=(t,e)=>`
  <div class="inst-code">
    <pre><code>${n(t)}</code></pre>
    <button type="button" class="inst-btn inst-copy" data-copy="${n(t)}" aria-label="${n(e)} 명령 복사">복사</button>
  </div>`,o=document.getElementById("setup-root");o&&(o.innerHTML=`
  <main class="inst-main">
    <p class="inst-back"><a href="./index.html">← 시뮬레이터로</a> · <a href="./install.html">시계에 펌웨어 설치</a> · <a href="./guide.html">따라 하기 안내서</a></p>
    <h1 class="inst-title">이 컴퓨터 세팅</h1>
    <p class="inst-lead">시계 <strong>실행 모드</strong> 앱 타일은 <code>Ctrl+Alt+숫자</code> 를 보냅니다(1 Claude · 2 카카오톡 · 6 한글 · 7 쿨메신저 — 나이스·유튜브·탐색기·바탕 화면·창 닫기는 설정 없이 됩니다). 그 키로 앱이 열리도록 이 PC 에 바로 가기를 한 번 만듭니다. <strong>새 컴퓨터마다 한 번</strong>이면 됩니다. 작업표시줄 순서·한/영 상태와 상관없이 동작합니다.</p>

    <p class="inst-ok">시계 설정 화면에서 <strong>이 컴퓨터 세팅</strong>을 누르면 이 PC 의 브라우저에 이 페이지가 열립니다(시계가 Win+R 로 주소를 칩니다). 한글 입력 상태면 주소가 깨질 수 있으니, 그때는 영문으로 바꾼 뒤 다시 누르세요.</p>

    <section class="inst-card" aria-labelledby="setup-s1">
      <h2 id="setup-s1"><span class="inst-n">1</span>스크립트 내려받기</h2>
      <p><a href="./pc-setup/wrist-shortcuts.ps1" download="wrist-shortcuts.ps1">wrist-shortcuts.ps1 내려받기</a> — PowerShell 스크립트입니다. 관리자 권한은 필요 없고, 내 시작 메뉴 <code>손목 컨트롤러</code> 폴더에 바로 가기 4개(1·2·6·7)를 만듭니다.</p>
    </section>

    <section class="inst-card" aria-labelledby="setup-s2">
      <h2 id="setup-s2"><span class="inst-n">2</span>실행</h2>
      <p>내려받은 파일을 <strong>오른쪽 클릭 → PowerShell 에서 실행</strong>. 실행이 막히면 내려받은 폴더에서 PowerShell 을 열고 아래 한 줄을 실행합니다.</p>
      ${p(r,"바로 가기 스크립트")}
    </section>

    <section class="inst-card" aria-labelledby="setup-s3">
      <h2 id="setup-s3"><span class="inst-n">3</span>확인</h2>
      <ol class="inst-steps">
        <li>창에 앱마다 <code>만듦</code> / <code>건너뜀</code> 이 표시됩니다. 건너뛴 앱은 시작 메뉴에서 찾지 못한 것입니다(그 앱을 설치한 뒤 스크립트를 다시 실행하면 됩니다 — 다시 실행하면 덮어씁니다).</li>
        <li>바로 가기 키가 바로 안 먹으면 <strong>로그아웃 후 다시 로그인</strong>합니다.</li>
        <li>시계 실행 모드에서 타일을 눌러 앱이 열리는지 확인합니다.</li>
      </ol>
      <p class="inst-sub">macOS 는 이 설정 없이 Spotlight 로 엽니다.</p>
    </section>

    <p class="inst-foot">이 페이지는 PC 에 바로 가기만 만듭니다. 시계 펌웨어 설치·백업은 <a href="./install.html">시계에 설치</a> 페이지에서 합니다.</p>
  </main>`,o.querySelectorAll(".inst-copy").forEach(t=>t.addEventListener("click",async()=>{var a;const e=t.dataset.copy??"";try{await navigator.clipboard.writeText(e),t.textContent="복사됨"}catch{const c=(a=t.parentElement)==null?void 0:a.querySelector("code");if(c){const l=document.createRange();l.selectNodeContents(c);const s=getSelection();s==null||s.removeAllRanges(),s==null||s.addRange(l)}t.textContent="선택됨 — Ctrl+C"}setTimeout(()=>t.textContent="복사",1600)})));
