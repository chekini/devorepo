(async () => {
  if (typeof html2canvas === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
    document.head.appendChild(script);
    await new Promise(res => script.onload = res);
  }

  const div = document.querySelector('.page-main.is-tab');
  if (!div) {
    console.error('No se encontró el div .page-main.is-tab');
    return;
  }

  const spans = document.querySelectorAll('span.multi-space');
  let texto = '';
  if (spans.length >= 2) {
    texto = spans[1].innerText.trim();
  } else {
    console.warn('No se encontró el segundo span.multi-space, se usará nombre por defecto');
    texto = 'captura';
  }

  // Limpiar texto para usarlo como nombre de archivo (quitar caracteres inválidos)
  const nombreArchivo = texto.replace(/[\\\/:*?"<>|]/g, '').slice(0, 30) || 'captura';

  html2canvas(div, { scale: 2 }).then(originalCanvas => {
    const fullWidth = originalCanvas.width;
    const fullHeight = originalCanvas.height;
    const halfHeight = Math.floor(fullHeight / 2);
    const extraRecorte = 50;
    const croppedHeight = halfHeight - extraRecorte;

    const canvas = document.createElement('canvas');
    canvas.width = fullWidth;
    canvas.height = croppedHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(originalCanvas, 0, 0, fullWidth, croppedHeight, 0, 0, fullWidth, croppedHeight);

    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `${nombreArchivo}.png`;
    a.click();
  });
})();
