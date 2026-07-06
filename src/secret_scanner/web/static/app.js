// ==========================================================================
// SecretScanner — Frontend Logic
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // Global App State
  const state = {
    totalScans: 0,
    totalSecretsFound: 0,
    totalHighRisk: 0,
    activeView: "panel-dashboard",
    lastPathScanResults: null,
    patterns: []
  };

  // Views Configuration (Title & Subtitle mapping)
  const viewMeta = {
    "panel-dashboard": {
      title: "Dashboard Principal",
      desc: "Resumen general e indicadores clave de seguridad de tu código."
    },
    "panel-path-scanner": {
      title: "Escáner de Directorios",
      desc: "Escanea carpetas del sistema local o archivos individuales recursivamente."
    },
    "panel-code-scanner": {
      title: "Escáner de Código (Copia y Pega)",
      desc: "Analiza fragmentos de código temporal o de logs de forma instantánea."
    },
    "panel-entropy": {
      title: "Analizador de Robustez y Entropía",
      desc: "Calcula la entropía de Shannon e inspecciona la resistencia de tus credenciales."
    },
    "panel-generator": {
      title: "Generador de Secretos Seguros",
      desc: "Genera claves de API, tokens o contraseñas criptográficamente seguras."
    },
    "panel-regex-lab": {
      title: "Laboratorio Regex",
      desc: "Prueba y diseña expresiones regulares personalizadas de búsqueda."
    },
    "panel-sandbox": {
      title: "Caja de Arena de Remediación",
      desc: "Guía interactiva sobre cómo asegurar tu código migrando secretos a entornos seguros."
    }
  };

  // Elements Selection
  const navItems = document.querySelectorAll(".nav-item");
  const panels = document.querySelectorAll(".content-panel");
  const viewTitle = document.getElementById("current-view-title");
  const viewDesc = document.getElementById("current-view-desc");

  // Load Active Patterns
  fetchActivePatterns();

  // Navigation Logic
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const target = item.getAttribute("data-target");
      if (!target) return;

      // Switch Active Nav Item
      navItems.forEach(i => i.classList.remove("active"));
      item.classList.add("active");

      // Switch Panels
      panels.forEach(p => p.classList.remove("active"));
      document.getElementById(target).classList.add("active");

      // Update Header Text
      if (viewMeta[target]) {
        viewTitle.textContent = viewMeta[target].title;
        viewDesc.textContent = viewMeta[target].desc;
      }

      state.activeView = target;
      
      // Auto-focus on inputs depending on screen load
      if (target === "panel-path-scanner") {
        document.getElementById("scan-path-input").focus();
      } else if (target === "panel-code-scanner") {
        document.getElementById("code-paste-input").focus();
      } else if (target === "panel-entropy") {
        document.getElementById("entropy-secret-input").focus();
      }
    });
  });

  // Fetch patterns from API to show in Dashboard
  async function fetchActivePatterns() {
    const listContainer = document.getElementById("active-patterns-summary");
    try {
      const response = await fetch("/api/patterns");
      if (!response.ok) throw new Error("No se pudieron cargar los patrones.");
      
      state.patterns = await response.json();
      document.getElementById("stat-patterns").textContent = state.patterns.length;
      
      listContainer.innerHTML = "";
      state.patterns.forEach(pat => {
        const row = document.createElement("div");
        row.className = "pattern-row";
        
        const severityClass = pat.severity.toLowerCase() === "high" ? "badge-high" : 
                              pat.severity.toLowerCase() === "medium" ? "badge-medium" : "badge-low";
        
        row.innerHTML = `
          <span class="pattern-name">${pat.name}</span>
          <span class="pattern-badge ${severityClass}">${pat.severity}</span>
        `;
        listContainer.appendChild(row);
      });
    } catch (err) {
      listContainer.innerHTML = `<div class="error-text">Error al cargar patrones: ${err.message}</div>`;
    }
  }


  // ================= 1. PATH SCANNER LOGIC =================
  const pathScanForm = document.getElementById("form-path-scan");
  const pathScanInput = document.getElementById("scan-path-input");
  const btnPathScan = document.getElementById("btn-path-scan");
  const pathScanLoading = document.getElementById("path-scan-loading");
  const pathScanResults = document.getElementById("path-scan-results");
  const pathFindingsBody = document.getElementById("path-scan-findings-body");
  const pathNoFindings = document.getElementById("path-scan-no-findings");

  // Sub-scanner navigation
  const btnSubTabs = document.querySelectorAll(".btn-sub-tab");
  const subScanContents = document.querySelectorAll(".sub-scan-content");

  // Detect environment (local vs cloud deployment)
  const isLocal = window.location.hostname === "localhost" || 
                  window.location.hostname === "127.0.0.1" || 
                  window.location.hostname === "[::1]" || 
                  window.location.hostname === "";

  if (!isLocal) {
    // Hide the local scan button
    const localBtn = document.querySelector('.btn-sub-tab[data-sub-scan="sub-scan-local"]');
    if (localBtn) {
      localBtn.style.display = "none";
      localBtn.classList.remove("active");
    }
    // De-activate local content
    const localContent = document.getElementById("sub-scan-local");
    if (localContent) {
      localContent.classList.remove("active");
    }
    // Activate GitHub tab by default in remote deployments
    const gitBtn = document.querySelector('.btn-sub-tab[data-sub-scan="sub-scan-github"]');
    const gitContent = document.getElementById("sub-scan-github");
    if (gitBtn && gitContent) {
      gitBtn.classList.add("active");
      gitContent.classList.add("active");
    }
  }

  btnSubTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("data-sub-scan");
      btnSubTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      subScanContents.forEach(c => c.classList.remove("active"));
      document.getElementById(targetId).classList.add("active");
    });
  });


  // Shared function to render findings
  function renderFindings(data) {
    state.lastPathScanResults = data;
    state.totalScans += 1;
    document.getElementById("stat-scans").textContent = state.totalScans;

    // Update summary cards
    document.getElementById("scan-res-files").textContent = data.total_files;
    document.getElementById("scan-res-count").textContent = data.findings.length;

    // Filter high/medium risk to update general stats
    let highRiskCount = 0;
    data.findings.forEach(f => {
      if (f.severity === "HIGH") highRiskCount++;
    });
    state.totalSecretsFound += data.findings.length;
    state.totalHighRisk += highRiskCount;
    
    document.getElementById("stat-secrets").textContent = state.totalSecretsFound;
    document.getElementById("stat-high").textContent = state.totalHighRisk;

    // Populate Findings Table
    pathFindingsBody.innerHTML = "";
    if (data.findings.length === 0) {
      pathNoFindings.classList.remove("hidden");
    } else {
      pathNoFindings.classList.add("hidden");
      data.findings.forEach(f => {
        const tr = document.createElement("tr");
        const severityClass = f.severity.toLowerCase() === "high" ? "badge-high" : 
                              f.severity.toLowerCase() === "medium" ? "badge-medium" : "badge-low";
        
        tr.innerHTML = `
          <td><span class="pattern-badge ${severityClass}">${f.severity}</span></td>
          <td><strong>${f.type}</strong></td>
          <td class="td-file">${getFileName(f.file)}:${f.line} <span class="tooltip-file" title="${f.file}">ℹ️</span></td>
          <td><div class="td-content">${escapeHTML(f.content)}</div></td>
        `;
        pathFindingsBody.appendChild(tr);
      });
    }

    pathScanResults.classList.remove("hidden");
  }

  // 1A. LOCAL SCAN SUBMIT
  pathScanForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const path = pathScanInput.value.trim();
    if (!path) return;

    pathScanLoading.classList.remove("hidden");
    pathScanResults.classList.add("hidden");
    btnPathScan.disabled = true;
    pathFindingsBody.innerHTML = "";
    pathNoFindings.classList.add("hidden");

    try {
      const response = await fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path: path })
      });

      if (!response.ok) {
        const errDetail = await response.json();
        throw new Error(errDetail.detail || "Error desconocido al escanear.");
      }

      const data = await response.json();
      renderFindings(data);
    } catch (err) {
      alert(`Error de Escaneo: ${err.message}`);
    } finally {
      pathScanLoading.classList.add("hidden");
      btnPathScan.disabled = false;
    }
  });

  // 1B. GITHUB SCAN SUBMIT
  const gitScanForm = document.getElementById("form-git-scan");
  const gitScanInput = document.getElementById("scan-git-input");
  const btnGitScan = document.getElementById("btn-git-scan");

  gitScanForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const cloneUrl = gitScanInput.value.trim();
    if (!cloneUrl) return;

    pathScanLoading.classList.remove("hidden");
    pathScanResults.classList.add("hidden");
    btnGitScan.disabled = true;
    pathFindingsBody.innerHTML = "";
    pathNoFindings.classList.add("hidden");

    try {
      const response = await fetch("/api/scan-git", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ clone_url: cloneUrl })
      });

      if (!response.ok) {
        const errDetail = await response.json();
        throw new Error(errDetail.detail || "Error al escanear repositorio de GitHub.");
      }

      const data = await response.json();
      renderFindings(data);
    } catch (err) {
      alert(`Error de GitHub Scan: ${err.message}`);
    } finally {
      pathScanLoading.classList.add("hidden");
      btnGitScan.disabled = false;
    }
  });

  // 1C. ZIP FILE UPLOAD SCAN
  const dragDropZone = document.getElementById("zip-drag-drop-zone");
  const zipFileInput = document.getElementById("zip-file-input");
  const fileSelectedStatus = document.getElementById("zip-file-selected-status");
  const zipFilenameLabel = document.getElementById("zip-filename-label");
  const btnUploadScan = document.getElementById("btn-upload-scan");
  const btnCancelUpload = document.getElementById("btn-cancel-upload");
  let selectedFile = null;

  // Open file browser on click
  dragDropZone.addEventListener("click", () => {
    zipFileInput.click();
  });

  // Handle selected file change
  zipFileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  // Drag & drop events
  dragDropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dragDropZone.classList.add("drag-over");
  });

  dragDropZone.addEventListener("dragleave", () => {
    dragDropZone.classList.remove("drag-over");
  });

  dragDropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dragDropZone.classList.remove("drag-over");
    if (e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  function handleFileSelected(file) {
    if (!file.name.endsWith(".zip")) {
      alert("Solo se permiten archivos comprimidos (.zip).");
      return;
    }
    selectedFile = file;
    zipFilenameLabel.textContent = `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    fileSelectedStatus.classList.remove("hidden");
    dragDropZone.classList.add("hidden");
  }

  btnCancelUpload.addEventListener("click", (e) => {
    e.stopPropagation();
    selectedFile = null;
    zipFileInput.value = "";
    fileSelectedStatus.classList.add("hidden");
    dragDropZone.classList.remove("hidden");
  });

  btnUploadScan.addEventListener("click", async () => {
    if (!selectedFile) return;

    pathScanLoading.classList.remove("hidden");
    pathScanResults.classList.add("hidden");
    btnUploadScan.disabled = true;
    pathFindingsBody.innerHTML = "";
    pathNoFindings.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("/api/scan-upload", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        const errDetail = await response.json();
        throw new Error(errDetail.detail || "Error al procesar archivo subido.");
      }

      const data = await response.json();
      renderFindings(data);
    } catch (err) {
      alert(`Error de Escaneo por Carga: ${err.message}`);
    } finally {
      pathScanLoading.classList.add("hidden");
      btnUploadScan.disabled = false;
    }
  });


  // Helpers
  function getFileName(filePath) {
    return filePath.split(/[/\\]/).pop();
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  // Export Results
  window.exportResults = function(format) {
    if (!state.lastPathScanResults || !state.lastPathScanResults.findings.length) {
      alert("No hay resultados de escaneo disponibles para exportar.");
      return;
    }
    const findings = state.lastPathScanResults.findings;
    
    if (format === "json") {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(findings, null, 2));
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "secret_scanner_report.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    } else if (format === "csv") {
      let csvContent = "data:text/csv;charset=utf-8,";
      csvContent += "Type,Severity,File,Line,Content\n";
      
      findings.forEach(f => {
        // Escape quotes
        const row = [
          `"${f.type}"`,
          `"${f.severity}"`,
          `"${f.file.replace(/"/g, '""')}"`,
          f.line,
          `"${f.content.replace(/"/g, '""')}"`
        ].join(",");
        csvContent += row + "\n";
      });

      const encodedUri = encodeURI(csvContent);
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", encodedUri);
      downloadAnchor.setAttribute("download", "secret_scanner_report.csv");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    }
  };


  // ================= 2. CODE SCANNER LOGIC =================
  const codePasteInput = document.getElementById("code-paste-input");
  const btnClearCode = document.getElementById("btn-clear-code");
  const btnCodeScan = document.getElementById("btn-code-scan");
  const codeScanResults = document.getElementById("code-scan-results");
  const codeResLines = document.getElementById("code-res-lines");
  const codeResCount = document.getElementById("code-res-count");
  const codeFindingsList = document.getElementById("code-findings-list");
  const codeViewerContainer = document.getElementById("code-viewer-container");

  btnClearCode.addEventListener("click", () => {
    codePasteInput.value = "";
    codeScanResults.classList.add("hidden");
    codePasteInput.focus();
  });

  btnCodeScan.addEventListener("click", async () => {
    const code = codePasteInput.value;
    if (!code.trim()) {
      alert("Por favor, pega algún fragmento de código primero.");
      return;
    }

    btnCodeScan.disabled = true;
    try {
      const response = await fetch("/api/scan-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code })
      });

      if (!response.ok) throw new Error("Error del servidor al escanear.");

      const data = await response.json();
      
      // Update counts
      codeResLines.textContent = data.total_lines;
      codeResCount.textContent = data.findings.length;

      // Populate findings mini list
      codeFindingsList.innerHTML = "";
      if (data.findings.length === 0) {
        codeFindingsList.innerHTML = `<div class="no-findings-alert">🎉 ¡No se encontraron credenciales críticas en tu fragmento de código!</div>`;
      } else {
        data.findings.forEach(f => {
          const item = document.createElement("div");
          item.className = "finding-mini-item";
          const severityClass = f.severity.toLowerCase() === "high" ? "badge-high" : 
                                f.severity.toLowerCase() === "medium" ? "badge-medium" : "badge-low";
          
          item.innerHTML = `
            <span class="mini-badge ${severityClass}">${f.severity}</span>
            <div class="mini-details">
              <span class="mini-title">${f.type}</span>
              <span class="mini-meta">Línea ${f.line}</span>
              <span class="mini-content">${escapeHTML(f.content)}</span>
            </div>
          `;
          codeFindingsList.appendChild(item);
        });
      }

      // Populate marked code viewer
      codeViewerContainer.innerHTML = "";
      const lines = code.split("\n");
      
      // Create a set of vulnerable lines
      const vulnLinesMap = {};
      data.findings.forEach(f => {
        vulnLinesMap[f.line] = f;
      });

      lines.forEach((lineText, index) => {
        const lineNum = index + 1;
        const lineRow = document.createElement("div");
        const isVuln = vulnLinesMap[lineNum] !== undefined;
        
        lineRow.className = `code-line-row ${isVuln ? "vulnerable-line" : ""}`;
        
        lineRow.innerHTML = `
          <span class="line-num-col">${lineNum}</span>
          <span class="line-content-col">${escapeHTML(lineText)}</span>
        `;
        
        codeViewerContainer.appendChild(lineRow);
      });

      codeScanResults.classList.remove("hidden");
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      btnCodeScan.disabled = false;
    }
  });


  // ================= 3. ENTROPY ANALYZER LOGIC =================
  const entropySecretInput = document.getElementById("entropy-secret-input");
  const btnEntropyRandom = document.getElementById("btn-entropy-random");
  const btnEntropyEval = document.getElementById("btn-entropy-eval");
  const entropyRecsList = document.getElementById("entropy-recs-list");
  const gaugeFill = document.getElementById("gauge-fill");
  const strengthLabel = document.getElementById("entropy-strength-label");
  const valueBits = document.getElementById("entropy-value-bits");
  const statShannonVal = document.getElementById("stat-shannon-val");
  const statCrackTime = document.getElementById("stat-crack-time");

  // Dice button: generates a mock vulnerable or random secret to test
  btnEntropyRandom.addEventListener("click", () => {
    const list = [
      "password123",
      "admin",
      "AKIAIOSFODNN7EXAMPLE",
      "Super_Pass_2026_@_Secure",
      "ghp_mZ93A8B10CdEfgH9IjkLmnOpQrStUvWxYz01",
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
      "123456"
    ];
    const rand = list[Math.floor(Math.random() * list.length)];
    entropySecretInput.value = rand;
    evaluateEntropy(rand);
  });

  btnEntropyEval.addEventListener("click", () => {
    const secret = entropySecretInput.value;
    evaluateEntropy(secret);
  });

  async function evaluateEntropy(secret) {
    if (!secret) {
      alert("Por favor, introduce un secreto o contraseña para analizar.");
      return;
    }

    try {
      const response = await fetch("/api/entropy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ secret: secret })
      });

      if (!response.ok) throw new Error("Error al consultar entropía.");

      const data = await response.json();
      
      // Update UI Text
      strengthLabel.textContent = data.strength;
      valueBits.textContent = `${data.pool_entropy_bits} bits`;
      statShannonVal.textContent = `${data.shannon_entropy} bits/caract.`;
      statCrackTime.textContent = data.crack_time_formatted;

      // Recommendations list
      entropyRecsList.innerHTML = "";
      data.recommendations.forEach(rec => {
        const li = document.createElement("li");
        li.textContent = rec;
        entropyRecsList.appendChild(li);
      });

      // Gauge Circular Animation
      // Full circle is 251.2 dashoffset. Max security reference is 120 bits.
      const bits = Math.min(120, data.pool_entropy_bits);
      const percentage = bits / 120;
      const offset = 251.2 - (percentage * 251.2);
      
      gaugeFill.style.strokeDashoffset = offset;

      // Color coding gauge class
      gaugeFill.className.baseVal = "gauge-fill";
      if (data.strength.includes("Muy Débil") || data.strength.includes("Débil")) {
        gaugeFill.classList.add("strength-weak");
        strengthLabel.style.color = "var(--color-rose)";
      } else if (data.strength.includes("Medio")) {
        gaugeFill.classList.add("strength-medium");
        strengthLabel.style.color = "var(--color-amber)";
      } else if (data.strength.includes("Fuerte") && !data.strength.includes("Muy")) {
        gaugeFill.classList.add("strength-strong");
        strengthLabel.style.color = "var(--color-sky)";
      } else {
        gaugeFill.classList.add("strength-very-strong");
        strengthLabel.style.color = "var(--color-emerald)";
      }

    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  }


  // ================= 4. SECRET GENERATOR LOGIC =================
  const genLength = document.getElementById("gen-length");
  const genLengthVal = document.getElementById("gen-length-val");
  const genUpper = document.getElementById("gen-upper");
  const genLower = document.getElementById("gen-lower");
  const genDigits = document.getElementById("gen-digits");
  const genSymbols = document.getElementById("gen-symbols");
  const btnGenerateAction = document.getElementById("btn-generate-action");
  const generatedSecretOutput = document.getElementById("generated-secret-output");
  const btnCopySecret = document.getElementById("btn-copy-secret");
  const genQuickAudit = document.getElementById("gen-quick-audit");

  genLength.addEventListener("input", (e) => {
    genLengthVal.textContent = e.target.value;
  });

  btnGenerateAction.addEventListener("click", async () => {
    const payload = {
      length: parseInt(genLength.value),
      use_upper: genUpper.checked,
      use_lower: genLower.checked,
      use_digits: genDigits.checked,
      use_symbols: genSymbols.checked
    };

    try {
      const response = await fetch("/api/generate-secret", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Error del servidor al generar secreto.");

      const data = await response.json();
      
      generatedSecretOutput.value = data.secret;
      
      // Update quick audit stats
      document.getElementById("gen-audit-bits").textContent = data.metrics.pool_entropy_bits;
      
      const strEl = document.getElementById("gen-audit-strength");
      strEl.textContent = data.metrics.strength;
      
      // Color key generator strength
      if (data.metrics.strength.includes("Débil")) strEl.style.color = "var(--color-rose)";
      else if (data.metrics.strength.includes("Medio")) strEl.style.color = "var(--color-amber)";
      else if (data.metrics.strength.includes("Fuerte") && !data.metrics.strength.includes("Muy")) strEl.style.color = "var(--color-sky)";
      else strEl.style.color = "var(--color-emerald)";

      document.getElementById("gen-audit-time").textContent = data.metrics.crack_time_formatted;
      
      genQuickAudit.classList.remove("hidden");

      // Reset copy button status
      btnCopySecret.textContent = "Copiar Secreto";
      btnCopySecret.className = "btn btn-copy";
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  });

  btnCopySecret.addEventListener("click", () => {
    const val = generatedSecretOutput.value;
    if (!val) return;

    navigator.clipboard.writeText(val).then(() => {
      btnCopySecret.textContent = "¡Copiado con éxito!";
      btnCopySecret.className = "btn btn-copy copied";
      setTimeout(() => {
        btnCopySecret.textContent = "Copiar Secreto";
        btnCopySecret.className = "btn btn-copy";
      }, 2000);
    });
  });


  // ================= 5. REGEX LAB LOGIC =================
  const regexPatternInput = document.getElementById("regex-pattern-input");
  const regexTestInput = document.getElementById("regex-test-input");
  const btnRegexTest = document.getElementById("btn-regex-test");
  const regexResultsBox = document.getElementById("regex-results-box");

  btnRegexTest.addEventListener("click", async () => {
    const pattern = regexPatternInput.value.trim();
    const text = regexTestInput.value;

    if (!pattern) {
      alert("Por favor, introduce una expresión regular.");
      return;
    }

    regexResultsBox.innerHTML = "<div class='loader-spinner small'></div>";
    regexResultsBox.classList.remove("empty");

    try {
      const response = await fetch("/api/patterns/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pattern: pattern, text: text })
      });

      if (!response.ok) {
        const errDetail = await response.json();
        throw new Error(errDetail.detail || "Error en regex.");
      }

      const data = await response.json();

      regexResultsBox.innerHTML = "";
      if (data.matches.length === 0) {
        regexResultsBox.innerHTML = "❌ Ninguna coincidencia encontrada. Verifica tu patrón de regex o tu texto.";
      } else {
        data.matches.forEach(m => {
          const item = document.createElement("div");
          item.className = "regex-match-item";
          
          item.innerHTML = `
            <div class="match-header">
              <span>Línea ${m.line} (Posición ${m.start} - ${m.end})</span>
            </div>
            <div class="match-text">${escapeHTML(m.match)}</div>
            <div class="match-content">${escapeHTML(m.content)}</div>
          `;
          
          regexResultsBox.appendChild(item);
        });
      }

    } catch (err) {
      regexResultsBox.innerHTML = `<div style="color: var(--color-rose);">⚠️ Error: ${err.message}</div>`;
    }
  });


  // ================= 6. REMEDIATION SANDBOX DATABASE =================
  const remediationDatabase = {
    python: {
      vuln: `import os
import requests

# ❌ VULNERABLE: Token hardcodeado directamente en el script
GITHUB_TOKEN = "ghp_mZ93A8B10CdEfgH9IjkLmnOpQrStUvWxYz01"

headers = {"Authorization": f"token {GITHUB_TOKEN}"}
r = requests.get("https://api.github.com/user", headers=headers)
print(r.json())`,
      sec: `import os
import requests
from dotenv import load_dotenv

# ✓ SEGURO: Carga las variables de entorno locales desde el archivo .env
load_dotenv()

# Recupera la clave desde el sistema en lugar del código fuente
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("ERROR: GITHUB_TOKEN no configurado en el sistema.")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}
r = requests.get("https://api.github.com/user", headers=headers)
print(r.json())`,
      steps: [
        { title: "Instalar librería dotenv", desc: "Instala la librería ejecutando el comando: <code>pip install python-dotenv</code>." },
        { title: "Crear archivo .env", desc: "Crea un archivo llamado <code>.env</code> en el directorio raíz de tu proyecto e ingresa tu secreto: <code>GITHUB_TOKEN=ghp_...</code>" },
        { title: "Ocultar .env del control de versiones", desc: "Agrega <code>.env</code> en tu archivo <code>.gitignore</code> para evitar que se cargue accidentalmente a repositorios como GitHub." },
        { title: "Cargar y recuperar", desc: "Llama a <code>load_dotenv()</code> en tu código fuente y accede de forma segura mediante <code>os.getenv('GITHUB_TOKEN')</code>." }
      ]
    },
    javascript: {
      vuln: `const { Client } = require('pg');

// ❌ VULNERABLE: Credenciales de producción expuestas en el código fuente
const client = new Client({
  host: 'db.production.servidor.com',
  user: 'superuser_admin',
  password: 'ProductionPassword2026_SecureKey!',
  database: 'ecommerce_prod'
});

client.connect();`,
      sec: `const { Client } = require('pg');
// ✓ SEGURO: Cargar configuración de ambiente usando dotenv
require('dotenv').config();

const client = new Client({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE
});

client.connect();`,
      steps: [
        { title: "Añadir paquete dotenv", desc: "Añade el módulo ejecutando: <code>npm install dotenv</code>." },
        { title: "Configurar archivo local .env", desc: "Crea el archivo <code>.env</code> con las variables: <code>DB_PASSWORD=contraseña</code>, <code>DB_HOST=servidor</code>, etc." },
        { title: "Proteger el archivo", desc: "Agrega una línea en tu archivo <code>.gitignore</code> conteniendo <code>.env</code>." },
        { title: "Llamar en el punto de entrada", desc: "Configura la lectura al inicio de tu app llamando a <code>require('dotenv').config()</code> y accede con <code>process.env.VARIABLE</code>." }
      ]
    },
    go: {
      vuln: `package main
import "github.com/aws/aws-sdk-go/aws"

func main() {
    // ❌ VULNERABLE: Llaves de AWS y accesos hardcodeados expuestos a fugas
    awsAccessKey := "AKIAIOSFODNN7EXAMPLE"
    awsSecretKey := "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    // ... lógica para inicializar AWS SDK ...
}`,
      sec: `package main
import (
    "os"
    "log"
    "github.com/joho/godotenv"
)

func main() {
    // ✓ SEGURO: Cargar archivo local .env en tiempo de desarrollo
    err := godotenv.Load()
    if err != nil {
        log.Println("No se encontró archivo .env, cargando variables globales")
    }

    // Cargar credenciales nativas del sistema operativo
    awsAccessKey := os.Getenv("AWS_ACCESS_KEY_ID")
    awsSecretKey := os.Getenv("AWS_SECRET_ACCESS_KEY")
    
    if awsAccessKey == "" || awsSecretKey == "" {
        log.Fatal("Faltan credenciales de AWS configuradas en el entorno")
    }
}`,
      steps: [
        { title: "Instalar el módulo", desc: "Ejecuta en consola: <code>go get github.com/joho/godotenv</code>." },
        { title: "Crear archivo .env", desc: "Añade a tu raíz un archivo <code>.env</code> con las variables <code>AWS_ACCESS_KEY_ID=...</code> y su clave secreta." },
        { title: "Ignorar archivo .env", desc: "Añade la regla de exclusión en tu archivo <code>.gitignore</code>." },
        { title: "Importar y verificar", desc: "Carga las variables llamando a <code>godotenv.Load()</code> y lee usando <code>os.Getenv('VARIABLE')</code>." }
      ]
    },
    java: {
      vuln: `import java.sql.Connection;
import java.sql.DriverManager;

public class ConexiónDB {
    // ❌ VULNERABLE: Credenciales de administrador quemadas en la clase
    private static final String URL = "jdbc:mysql://localhost:3306/db";
    private static final String USER = "db_user";
    private static final String PASS = "DatabaseRootPassword987!";

    public Connection getConnection() throws Exception {
        return DriverManager.getConnection(URL, USER, PASS);
    }
}`,
      sec: `import java.sql.Connection;
import java.sql.DriverManager;
import io.github.cdimascio.dotenv.Dotenv;

public class ConexiónDB {
    // ✓ SEGURO: Recuperar llaves mediante biblioteca Dotenv-Java
    private static final Dotenv dotenv = Dotenv.load();
    
    private static final String URL = dotenv.get("DB_URL");
    private static final String USER = dotenv.get("DB_USER");
    private static final String PASS = dotenv.get("DB_PASS");

    public Connection getConnection() throws Exception {
        if (PASS == null) {
            throw new IllegalStateException("Variable DB_PASS no configurada.");
        }
        return DriverManager.getConnection(URL, USER, PASS);
    }
}`,
      steps: [
        { title: "Añadir dependencia Dotenv", desc: "Agrega la dependencia <code>dotenv-java</code> en tu archivo Maven <code>pom.xml</code> o Gradle." },
        { title: "Crear configuración .env", desc: "Crea el archivo <code>.env</code> con tu clave de conexión: <code>DB_PASS=DatabaseRootPassword987!</code>." },
        { title: "Agregar exclusión Git", desc: "Agrega <code>.env</code> en el archivo <code>.gitignore</code>." },
        { title: "Cargar valores", desc: "Instancia <code>Dotenv dotenv = Dotenv.load()</code> y recupera con <code>dotenv.get('VARIABLE')</code>." }
      ]
    }
  };

  const btnLangs = document.querySelectorAll(".btn-lang");
  const codeVuln = document.getElementById("remediation-vulnerable-code");
  const codeSec = document.getElementById("remediation-secure-code");
  const stepsDescription = document.getElementById("remediation-steps-description");

  // Load selected language remediation data
  function loadRemediation(lang) {
    const data = remediationDatabase[lang];
    if (!data) return;

    // Reset lang selector active status
    btnLangs.forEach(b => {
      if (b.getAttribute("data-lang") === lang) b.classList.add("active");
      else b.classList.remove("active");
    });

    codeVuln.textContent = data.vuln;
    codeSec.textContent = data.sec;

    // Populate steps
    stepsDescription.innerHTML = "";
    data.steps.forEach((step, idx) => {
      const stepRow = document.createElement("div");
      stepRow.className = "rem-step-item";
      stepRow.innerHTML = `
        <div class="step-number">${idx + 1}</div>
        <div class="step-details">
          <strong>${step.title}</strong>
          <p>${step.desc}</p>
        </div>
      `;
      stepsDescription.appendChild(stepRow);
    });
  }

  // Bind clicks for remediation tabs
  btnLangs.forEach(btn => {
    btn.addEventListener("click", () => {
      const lang = btn.getAttribute("data-lang");
      loadRemediation(lang);
    });
  });

  // Load default language (python) on startup
  loadRemediation("python");

});
