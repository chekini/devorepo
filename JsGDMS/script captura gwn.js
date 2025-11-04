(async () => {
  // Función delay para esperar ms
  const delay = ms => new Promise(res => setTimeout(res, ms));

  // Cargar html2canvas si no está
  if (typeof html2canvas === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
    document.head.appendChild(script);
    await new Promise(res => script.onload = res);
  }

  // Función para capturar y descargar div.page-main.is-tab con nombre basado en primer span.multi-space
  async function capturarYClicarMultiSpace() {
    const div = document.querySelector('.page-main.is-tab');
    if (!div) {
      console.error('No se encontró div.page-main.is-tab');
      return;
    }

    // Obtener texto primer span.multi-space
    const firstSpan = document.querySelector('span.multi-space');
    //const texto = firstSpan ? firstSpan.innerText.trim() : 'captura';
    //TEST
    const spans = document.querySelectorAll('span.multi-space');
    let texto = '';
    if (spans.length >= 2) {
      texto = spans[1].innerText.trim();
    } else {
      console.warn('No se encontró el segundo span.multi-space, se usará nombre por defecto');
      texto = 'captura';
    }
    // Limpiar nombre archivo
    const nombreArchivo = texto.replace(/[\\\/:*?"<>|]/g, '').slice(12,100) || 'captura';

    // Capturar con html2canvas
    const originalCanvas = await html2canvas(div, { scale: 2 });

    // Preparar canvas recortado (mitad superior - 50px)
    const fullWidth = originalCanvas.width;
    const fullHeight = originalCanvas.height;
    const halfHeight = Math.floor(fullHeight / 2);
    const extraRecorte = 132;
    const croppedHeight = halfHeight - extraRecorte;

    const canvas = document.createElement('canvas');
    canvas.width = fullWidth;
    canvas.height = croppedHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(originalCanvas, 0, 0, fullWidth, croppedHeight, 0, 0, fullWidth, croppedHeight);

    // Descargar imagen
    const a = document.createElement('a');
    a.href = canvas.toDataURL('image/png');
    a.download = `${nombreArchivo}.png`;
    a.click();

    // Dar click al primer span.multi-space
    if (firstSpan) {
      firstSpan.click();
    }
  }

  // Buscar tabla y filas
  const tabla = document.querySelector('.el-table__body tbody');
  if (!tabla) {
    console.error('No se encontró tbody dentro de .el-table__body');
    return;
  }
  const filas = Array.from(tabla.querySelectorAll('tr'));
  if (filas.length === 0) {
    console.warn('No hay filas en la tabla');
    return;
  }

  for (const fila of filas) {
    // Click en fila
    fila.click();
    await delay(2000);

    // Buscar span.el-radio-button__inner con texto "1 mes"
    const radios = Array.from(document.querySelectorAll('span.el-radio-button__inner'));
    const radio1Mes = radios.find(r => r.innerText.trim() === '1 mes');
    if (radio1Mes) {
      radio1Mes.click();
    } else {
      console.warn('No se encontró span.el-radio-button__inner con texto "1 mes"');
    }
    await delay(2000);

    // Capturar y dar click en span.multi-space
    await capturarYClicarMultiSpace();
  }

  console.log('Proceso terminado.');
})();
