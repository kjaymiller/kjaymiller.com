// Finds fenced code blocks written as ```strudel in markdown (rendered as
// <pre><code class="language-strudel">) and appends a link that opens the
// same code, pre-filled, in the strudel.cc REPL — using strudel's own
// share-link format: "#" + encodeURIComponent(btoa(JSON.stringify(code))).
(function () {
  function strudelLink(code) {
    const hash = encodeURIComponent(btoa(JSON.stringify(code)));
    return `https://strudel.cc/#${hash}`;
  }

  function init() {
    const blocks = document.querySelectorAll(
      'pre > code[class*="language-strudel"], pre > code.strudel'
    );
    blocks.forEach((code) => {
      const pre = code.parentElement;
      if (!pre || pre.dataset.strudelLinked) return;
      pre.dataset.strudelLinked = "true";

      const link = document.createElement("a");
      link.className = "strudel-link";
      link.href = strudelLink(code.textContent.trim());
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = "▶ Open in Strudel";

      pre.insertAdjacentElement("afterend", link);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
