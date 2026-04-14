from __future__ import annotations


def render_home_page() -> str:
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Boolish Helper</title>
  <style>
    :root {
      --bg: #f4efe7;
      --surface: #fffcf6;
      --ink: #152238;
      --muted: #5a6473;
      --primary: #0f766e;
      --primary-dark: #115e59;
      --border: #d8cec0;
      --warning: #9a3412;
      --radius: 14px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, sans-serif;
      background: radial-gradient(circle at top left, #fff6e2 0%, var(--bg) 45%, #ece8df 100%);
      color: var(--ink);
    }
    .container {
      max-width: 1120px;
      margin: 32px auto;
      padding: 20px;
    }
    h1 { margin: 0 0 8px; }
    p { color: var(--muted); margin-top: 0; }
    .tabs {
      display: flex;
      gap: 8px;
      margin: 20px 0 16px;
    }
    .tab-btn {
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--ink);
      border-radius: 999px;
      padding: 8px 16px;
      font-weight: 600;
      cursor: pointer;
    }
    .tab-btn.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary-dark);
    }
    .tab-panel {
      display: none;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
    }
    .tab-panel.active { display: block; }
    label {
      display: block;
      margin-top: 14px;
      margin-bottom: 6px;
      font-weight: 600;
    }
    textarea, input {
      width: 100%;
      border-radius: 10px;
      border: 1px solid var(--border);
      padding: 10px;
      font-size: 14px;
      background: #ffffff;
    }
    textarea {
      min-height: 220px;
      resize: vertical;
      font-family: Consolas, "Courier New", monospace;
    }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    button[type="submit"] {
      margin-top: 16px;
      border: none;
      border-radius: 10px;
      background: var(--primary);
      color: white;
      padding: 11px 14px;
      font-weight: 700;
      cursor: pointer;
    }
    button[type="submit"]:disabled { opacity: 0.7; cursor: not-allowed; }
    .status { margin-top: 14px; font-weight: 600; }
    .status.error { color: var(--warning); }
    .results { margin-top: 14px; display: none; }
    .links { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
    .links a {
      text-decoration: none;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: white;
      color: var(--ink);
      font-weight: 600;
    }
    .query-box {
      margin-top: 12px;
      display: none;
    }
    .query-box textarea {
      min-height: 90px;
    }
    .copy-btn {
      margin-top: 8px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: white;
      padding: 8px 10px;
      cursor: pointer;
      font-weight: 600;
    }
    iframe {
      width: 100%;
      min-height: 560px;
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-top: 12px;
      background: white;
    }
    @media (max-width: 760px) {
      .row { grid-template-columns: 1fr; }
      .container { margin: 16px auto; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Boolish Helper</h1>
    <p>Ferramentas modulares de apoio ad hoc para tarefas operacionais e pessoais.</p>

    <div class="tabs">
      <button class="tab-btn active" data-tab="coord-geohash">Coord -> Geohash</button>
      <button class="tab-btn" data-tab="coming-soon">Em Breve</button>
    </div>

    <section id="coord-geohash" class="tab-panel active">
      <h2>Coord para Geohash</h2>
      <p>Cole coordenadas em linhas no formato <code>lon, lat</code>.</p>
      <form id="coordForm">
        <label for="raw_coords">Coordenadas</label>
        <textarea id="raw_coords" name="raw_coords" placeholder="-46.67, -23.50&#10;-46.68, -23.51" required></textarea>
        <div class="row">
          <div>
            <label for="target_precision">Nivel geohash</label>
            <input id="target_precision" name="target_precision" type="number" min="4" max="12" step="1" value="5" required />
          </div>
          <div>
            <label for="max_outside">Max outside (0 a 1)</label>
            <input id="max_outside" name="max_outside" type="number" min="0" max="1" step="0.01" value="1" required />
          </div>
        </div>
        <button type="submit" id="submitBtn">Gerar mapa e geohashes</button>
      </form>
      <div id="status" class="status"></div>
      <div id="results" class="results">
        <div id="summary"></div>
        <div class="links">
          <a id="mapLink" href="#" target="_blank" rel="noopener noreferrer">Abrir mapa em nova aba</a>
          <a id="xlsxLink" href="#" target="_blank" rel="noopener noreferrer">Baixar XLSX</a>
        </div>
        <iframe id="mapFrame" title="Mapa de geohashes"></iframe>
      </div>
      <div id="queryBox" class="query-box">
        <label for="geohashQueryOutput">Geohashes para query (copiar e colar)</label>
        <textarea id="geohashQueryOutput" readonly></textarea>
        <button id="copyGeohashesBtn" class="copy-btn" type="button">Copiar geohashes</button>
      </div>
    </section>

    <section id="coming-soon" class="tab-panel">
      <h2>Em Breve</h2>
      <p>Espaco reservado para novas funcoes em sub-URLs dedicadas.</p>
    </section>
  </div>

  <script>
    const tabButtons = Array.from(document.querySelectorAll('.tab-btn'));
    const tabPanels = Array.from(document.querySelectorAll('.tab-panel'));
    tabButtons.forEach((button) => {
      button.addEventListener('click', () => {
        tabButtons.forEach((btn) => btn.classList.remove('active'));
        tabPanels.forEach((panel) => panel.classList.remove('active'));
        button.classList.add('active');
        document.getElementById(button.dataset.tab).classList.add('active');
      });
    });

    const form = document.getElementById('coordForm');
    const submitBtn = document.getElementById('submitBtn');
    const statusEl = document.getElementById('status');
    const resultsEl = document.getElementById('results');
    const summaryEl = document.getElementById('summary');
    const mapLink = document.getElementById('mapLink');
    const xlsxLink = document.getElementById('xlsxLink');
    const mapFrame = document.getElementById('mapFrame');
    const queryBoxEl = document.getElementById('queryBox');
    const geohashQueryOutputEl = document.getElementById('geohashQueryOutput');
    const copyGeohashesBtn = document.getElementById('copyGeohashesBtn');

    copyGeohashesBtn.addEventListener('click', async () => {
      const text = geohashQueryOutputEl.value;
      if (!text) return;

      try {
        await navigator.clipboard.writeText(text);
        copyGeohashesBtn.textContent = 'Copiado';
        setTimeout(() => { copyGeohashesBtn.textContent = 'Copiar geohashes'; }, 1200);
      } catch (_) {
        geohashQueryOutputEl.select();
        document.execCommand('copy');
      }
    });

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      statusEl.textContent = 'Processando...';
      statusEl.className = 'status';
      resultsEl.style.display = 'none';
      queryBoxEl.style.display = 'none';
      geohashQueryOutputEl.value = '';
      submitBtn.disabled = true;

      const payload = {
        raw_coords: form.raw_coords.value,
        target_precision: Number(form.target_precision.value),
        max_outside: Number(form.max_outside.value),
      };

      try {
        const response = await fetch('/api/coord-to-geohash/run', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Falha ao processar a requisicao.');
        }

        const mapUrl = `/api/coord-to-geohash/${data.run_id}/map`;
        const xlsxUrl = `/api/coord-to-geohash/${data.run_id}/xlsx`;

        mapLink.href = mapUrl;
        xlsxLink.href = xlsxUrl;
        mapFrame.src = mapUrl;
        summaryEl.innerHTML = `
          <strong>Total de geohashes:</strong> ${data.geohash_count}<br/>
          <strong>Rings detectados:</strong> ${data.rings_count}<br/>
          <strong>Stats por tamanho:</strong> ${JSON.stringify(data.stats_by_length)}
        `;
        geohashQueryOutputEl.value = data.geohashes.map((geohash) => `'${geohash}'`).join(', ');

        statusEl.textContent = 'Concluido.';
        resultsEl.style.display = 'block';
        queryBoxEl.style.display = 'block';
      } catch (error) {
        statusEl.textContent = error.message;
        statusEl.className = 'status error';
        queryBoxEl.style.display = 'none';
      } finally {
        submitBtn.disabled = false;
      }
    });
  </script>
</body>
</html>"""
