// Finds fenced code blocks written as ```strudel in markdown (rendered as
// <pre><code class="language-strudel">) and appends a link that opens the
// same code, pre-filled, in the strudel.cc REPL — using strudel's own
// share-link format: "#" + encodeURIComponent(unicodeToBase64(code)), where
// unicodeToBase64 base64-encodes the UTF-8 bytes of the raw code string
// (see @strudel/core's code2hash — it does NOT JSON.stringify the code).
(function () {
  function unicodeToBase64(text) {
    const utf8Bytes = new TextEncoder().encode(text);
    let binaryString = "";
    const chunkSize = 0x8000;
    for (let i = 0; i < utf8Bytes.length; i += chunkSize) {
      const chunk = utf8Bytes.subarray(i, i + chunkSize);
      binaryString += String.fromCharCode.apply(null, chunk);
    }
    return btoa(binaryString);
  }

  function strudelLink(code) {
    const hash = encodeURIComponent(unicodeToBase64(code));
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
