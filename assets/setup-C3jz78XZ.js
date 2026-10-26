import{s as l}from"./pwa-CC5vbYkQ.js";/* empty css                */l();const r="powershell -ExecutionPolicy Bypass -File .\\wrist-shortcuts.ps1",n=t=>t.replace(/[&<>"']/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[e]);try{const t=localStorage.getItem("wrist-sim.theme");(t==="light"||t==="dark")&&(document.documentElement.dataset.theme=t)}catch{}const p=(t,e)=>`
  <div class="inst-code">
    <pre><code>${n(t)}</code></pre>
    <button type="button" class="inst-btn inst-copy" data-copy="${n(t)}" aria-label="${n(e)} 명령 복사">복사</button>
  </div>`,a=document.getElementById("setup-root");a&&(a.innerHTML=`
  <main class="inst-main">
    <p class="inst-back"><a href="./index.html">← 시뮬레이터로</a> · <a href="./install.html">시계에 펌웨어 설치</a> · <a href="./guide.html">따라 하기 안내서</a></p>
    <h1 class="inst-title">이 컴퓨터 세팅</h1>
    <p class="inst-lead"><strong>설정할 것이 없습니다.</strong> 실행 타일은 PC 에 아무것도 깔지 않아도 됩니다. 시계가 실행 창(Win+R)에 명령을 넣어 시작 메뉴에서 그 앱을 찾아 엽니다. 설치되지 않은 앱은 열리지 않습니다. 실행 창이 한글 입력 상태면 글자가 깨질 수 있으니 처음 한 번 한/영을 확인하세요.</p>

    <p class="inst-ok">시계 설정 화면에서 <strong>이 컴퓨터 세팅</strong>을 누르면 이 PC 의 브라우저에 이 페이지가 열립니다(시계가 Win+R 로 주소를 칩니다). 이 페이지가 제대로 열렸다면 실행 창 한/영도 괜찮은 것입니다.</p>

    <section class="inst-card" aria-labelledby="setup-s1">
      <h2 id="setup-s1"><span class="inst-n">1</span>확인</h2>
      <ol class="inst-steps">
        <li>시계 실행 모드에서 Claude·카카오톡·한글·쿨메신저 타일을 눌러 앱이 열리는지 확인합니다. 실행 창이 잠깐 떴다가 앱이 열립니다.</li>
        <li>안 열리면 ① 그 앱이 이 PC 에 설치되어 있는지(시작 메뉴에서 찾아지는지), ② 실행 창이 한글 입력 상태가 아닌지 확인합니다.</li>
        <li>나이스·유튜브(주소), 탐색기·바탕 화면·창 닫기(Windows 기본 키)도 설정 없이 됩니다.</li>
      </ol>
      <p class="inst-sub">macOS 는 Spotlight 로 엽니다.</p>
    </section>

    <section class="inst-card" aria-labelledby="setup-s2">
      <h2 id="setup-s2"><span class="inst-n">2</span>예전 방식(선택, 이제 필요 없음)</h2>
      <p class="inst-sub">옛 펌웨어는 바로 가기 키를 보냈기 때문에 PC 마다 스크립트가 필요했습니다. 새 펌웨어에서는 실행하지 않아도 됩니다. 옛 펌웨어를 쓰는 경우에만: <a href="./pc-setup/wrist-shortcuts.ps1" download="wrist-shortcuts.ps1">wrist-shortcuts.ps1 내려받기</a> → 오른쪽 클릭 → PowerShell 에서 실행(막히면 아래 한 줄).</p>
      ${p(r,"옛 바로 가기 스크립트")}
      <p class="inst-sub">예전에 만든 시작 메뉴 <code>손목 컨트롤러</code> 폴더는 지워도 됩니다.</p>
    </section>

    <p class="inst-foot">이 페이지는 PC 쪽 안내만 합니다. 시계 펌웨어 설치·백업은 <a href="./install.html">시계에 설치</a> 페이지에서 합니다.</p>
  </main>`,a.querySelectorAll(".inst-copy").forEach(t=>t.addEventListener("click",async()=>{var o;const e=t.dataset.copy??"";try{await navigator.clipboard.writeText(e),t.textContent="복사됨"}catch{const c=(o=t.parentElement)==null?void 0:o.querySelector("code");if(c){const i=document.createRange();i.selectNodeContents(c);const s=getSelection();s==null||s.removeAllRanges(),s==null||s.addRange(i)}t.textContent="선택됨 — Ctrl+C"}setTimeout(()=>t.textContent="복사",1600)})));
