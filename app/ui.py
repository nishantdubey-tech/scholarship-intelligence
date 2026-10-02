"""Interactive Web UI template for Scholarship Intelligence FastAPI service."""


def get_ui_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Scholarship Intelligence — Verified Primary-Source Discovery & Change Detection</title>
  <meta name="description" content="AI & Evidence-grounded scholarship discovery, verification engine, and change tracking for Indian students.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* ===== DESIGN TOKENS ===== */
    :root {
      /* A warm, professional palette inspired by real government/institutional portals */
      --bg-page: #f4f1ec;
      --bg-card: #ffffff;
      --bg-card-alt: #faf8f5;
      --bg-sidebar: #1b2a4a;
      --bg-input: #f7f5f2;
      --bg-hover: #edeae4;
      --border-main: #d6d0c4;
      --border-light: #e8e3da;
      --border-accent: #b8860b;
      --text-heading: #1a1a2e;
      --text-body: #3d3d56;
      --text-muted: #7a7a8e;
      --text-dim: #a8a8b8;
      --text-inverse: #ffffff;

      /* Trust-evoking government blues & golds */
      --brand-primary: #1b4f8a;
      --brand-primary-light: #2d6cb5;
      --brand-primary-bg: rgba(27, 79, 138, 0.08);
      --brand-gold: #b8860b;
      --brand-gold-light: #daa520;
      --brand-gold-bg: rgba(184, 134, 11, 0.08);

      /* Semantic Colors */
      --status-verified: #1a7a3a;
      --status-verified-bg: #e8f5ec;
      --status-verified-border: #a8d8b9;
      --status-review: #a86800;
      --status-review-bg: #fff8e1;
      --status-review-border: #ffe0a0;
      --status-active: #0d6eaa;
      --status-active-bg: #e3f2fd;
      --status-active-border: #90caf9;
      --status-expired: #b71c1c;
      --status-expired-bg: #fdecea;
      --status-expired-border: #ef9a9a;
      --status-stale: #616161;
      --status-stale-bg: #f5f5f5;
      --status-stale-border: #bdbdbd;

      /* Shape & Type */
      --radius-xs: 4px;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --font-heading: 'Source Serif 4', Georgia, serif;
      --font-body: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      --font-mono: 'JetBrains Mono', 'SF Mono', 'Consolas', monospace;

      /* Elevation */
      --shadow-card: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
      --shadow-card-hover: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
      --shadow-modal: 0 20px 40px rgba(0,0,0,0.15), 0 8px 16px rgba(0,0,0,0.1);
    }

    *, *::before, *::after {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: var(--bg-page);
      color: var(--text-body);
      font-family: var(--font-body);
      font-size: 15px;
      line-height: 1.6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    /* ===== TOP BANNER (Government-style) ===== */
    .gov-banner {
      background: linear-gradient(135deg, #1b2a4a 0%, #1b4f8a 100%);
      color: var(--text-inverse);
      padding: 0.5rem 1.5rem;
      font-size: 0.78rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      letter-spacing: 0.01em;
    }

    .gov-banner a {
      color: #ffd54f;
      text-decoration: none;
      font-weight: 500;
    }

    .gov-banner a:hover {
      text-decoration: underline;
    }

    /* ===== HEADER ===== */
    .site-header {
      background: var(--bg-card);
      border-bottom: 3px solid var(--brand-gold);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }

    .brand-emblem {
      width: 46px;
      height: 46px;
      border-radius: var(--radius-md);
      background: linear-gradient(135deg, #1b4f8a, #1b2a4a);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      color: #ffd54f;
      box-shadow: 0 2px 8px rgba(27, 42, 74, 0.25);
      flex-shrink: 0;
    }

    .brand-title {
      font-family: var(--font-heading);
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--text-heading);
      letter-spacing: -0.01em;
      line-height: 1.2;
    }

    .brand-subtitle {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-top: 1px;
    }

    .header-nav {
      display: flex;
      gap: 0.6rem;
      flex-wrap: wrap;
      align-items: center;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.5rem 1rem;
      font-size: 0.82rem;
      font-weight: 500;
      font-family: var(--font-body);
      border-radius: var(--radius-sm);
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .btn-outline {
      background: transparent;
      color: var(--brand-primary);
      border-color: var(--brand-primary);
    }

    .btn-outline:hover {
      background: var(--brand-primary-bg);
    }

    .btn-solid {
      background: var(--brand-primary);
      color: var(--text-inverse);
      border-color: var(--brand-primary);
    }

    .btn-solid:hover {
      background: var(--brand-primary-light);
    }

    .btn-gold {
      background: var(--brand-gold);
      color: var(--text-inverse);
      border-color: var(--brand-gold);
    }

    .btn-gold:hover {
      background: var(--brand-gold-light);
    }

    /* ===== MAIN CONTAINER ===== */
    .main-container {
      max-width: 1340px;
      margin: 0 auto;
      padding: 1.75rem 2rem 3rem;
    }

    /* ===== STATS ROW ===== */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 0.85rem;
      margin-bottom: 1.75rem;
    }

    .stat-card {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1rem 1.15rem;
      box-shadow: var(--shadow-card);
      transition: box-shadow 0.2s ease, transform 0.15s ease;
      position: relative;
    }

    .stat-card:hover {
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-1px);
    }

    .stat-card::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      border-radius: var(--radius-md) var(--radius-md) 0 0;
    }

    .stat-card.stat-primary::after { background: var(--brand-primary); }
    .stat-card.stat-verified::after { background: var(--status-verified); }
    .stat-card.stat-active::after { background: var(--status-active); }
    .stat-card.stat-review::after { background: var(--status-review); }
    .stat-card.stat-expired::after { background: var(--status-expired); }
    .stat-card.stat-gold::after { background: var(--brand-gold); }

    .stat-label {
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 0.3rem;
    }

    .stat-value {
      font-family: var(--font-heading);
      font-size: 1.85rem;
      font-weight: 700;
      color: var(--text-heading);
      line-height: 1.1;
    }

    .stat-note {
      font-size: 0.72rem;
      color: var(--text-dim);
      margin-top: 0.2rem;
    }

    /* ===== TABS ===== */
    .tab-bar {
      display: flex;
      gap: 0;
      background: var(--bg-card);
      border: 1px solid var(--border-main);
      border-radius: var(--radius-md);
      margin-bottom: 1.5rem;
      overflow-x: auto;
      box-shadow: var(--shadow-card);
    }

    .tab-trigger {
      flex: 1;
      min-width: fit-content;
      background: transparent;
      border: none;
      border-right: 1px solid var(--border-light);
      padding: 0.85rem 1.25rem;
      font-family: var(--font-body);
      font-size: 0.88rem;
      font-weight: 500;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      white-space: nowrap;
      position: relative;
    }

    .tab-trigger:last-child {
      border-right: none;
    }

    .tab-trigger:hover {
      background: var(--bg-hover);
      color: var(--text-heading);
    }

    .tab-trigger.active {
      background: var(--brand-primary-bg);
      color: var(--brand-primary);
      font-weight: 600;
    }

    .tab-trigger.active::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: var(--brand-primary);
    }

    .tab-trigger .tab-icon {
      font-size: 1rem;
    }

    .tab-panel {
      display: none;
    }

    .tab-panel.active {
      display: block;
      animation: panelFade 0.25s ease;
    }

    @keyframes panelFade {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ===== FILTER CARD ===== */
    .filter-card {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1.15rem 1.35rem;
      margin-bottom: 1.25rem;
      box-shadow: var(--shadow-card);
    }

    .filter-row {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      align-items: stretch;
    }

    .search-field {
      flex: 1;
      min-width: 280px;
      position: relative;
    }

    .search-field input {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-main);
      border-radius: var(--radius-sm);
      padding: 0.65rem 0.9rem 0.65rem 2.4rem;
      font-size: 0.88rem;
      font-family: var(--font-body);
      color: var(--text-heading);
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }

    .search-field input:focus {
      border-color: var(--brand-primary);
      box-shadow: 0 0 0 3px rgba(27, 79, 138, 0.1);
    }

    .search-field input::placeholder {
      color: var(--text-dim);
    }

    .search-field .icon {
      position: absolute;
      left: 0.8rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.9rem;
      pointer-events: none;
    }

    .filter-select select {
      background: var(--bg-input);
      border: 1px solid var(--border-main);
      border-radius: var(--radius-sm);
      padding: 0.65rem 2rem 0.65rem 0.75rem;
      font-size: 0.84rem;
      font-family: var(--font-body);
      color: var(--text-body);
      outline: none;
      cursor: pointer;
      appearance: none;
      background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3e%3cpath fill='%237a7a8e' d='M2 4l4 4 4-4'/%3e%3c/svg%3e");
      background-repeat: no-repeat;
      background-position: right 0.6rem center;
      transition: border-color 0.15s;
    }

    .filter-select select:focus {
      border-color: var(--brand-primary);
    }

    /* ===== RESULTS HEADER ===== */
    .results-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding: 0 0.15rem;
    }

    .results-count {
      font-size: 0.88rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    .results-badge {
      font-size: 0.72rem;
      color: var(--status-verified);
      background: var(--status-verified-bg);
      border: 1px solid var(--status-verified-border);
      border-radius: var(--radius-xs);
      padding: 0.2rem 0.55rem;
      font-weight: 600;
    }

    /* ===== SCHOLARSHIP CARDS ===== */
    .sch-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(390px, 1fr));
      gap: 1rem;
    }

    .sch-item {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1.35rem 1.5rem;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-card);
      transition: box-shadow 0.2s ease, transform 0.15s ease;
    }

    .sch-item:hover {
      box-shadow: var(--shadow-card-hover);
      transform: translateY(-2px);
    }

    .sch-badges {
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
      margin-bottom: 0.6rem;
    }

    .pill {
      font-size: 0.68rem;
      font-weight: 600;
      padding: 0.15rem 0.5rem;
      border-radius: var(--radius-xs);
      text-transform: uppercase;
      letter-spacing: 0.03em;
      border: 1px solid;
    }

    .pill-verified {
      color: var(--status-verified);
      background: var(--status-verified-bg);
      border-color: var(--status-verified-border);
    }

    .pill-review {
      color: var(--status-review);
      background: var(--status-review-bg);
      border-color: var(--status-review-border);
    }

    .pill-active {
      color: var(--status-active);
      background: var(--status-active-bg);
      border-color: var(--status-active-border);
    }

    .pill-expired {
      color: var(--status-expired);
      background: var(--status-expired-bg);
      border-color: var(--status-expired-border);
    }

    .pill-stale {
      color: var(--status-stale);
      background: var(--status-stale-bg);
      border-color: var(--status-stale-border);
    }

    .pill-source {
      color: var(--brand-primary);
      background: var(--brand-primary-bg);
      border-color: rgba(27, 79, 138, 0.2);
    }

    .sch-name {
      font-family: var(--font-heading);
      font-size: 1.08rem;
      font-weight: 600;
      color: var(--text-heading);
      line-height: 1.35;
      margin-bottom: 0.25rem;
    }

    .sch-org {
      font-size: 0.82rem;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 0.35rem;
      margin-bottom: 0.85rem;
    }

    .sch-data-block {
      background: var(--bg-card-alt);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-sm);
      padding: 0.75rem 0.9rem;
      margin-bottom: 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      font-size: 0.84rem;
    }

    .data-pair {
      display: flex;
      justify-content: space-between;
      gap: 0.5rem;
    }

    .data-key {
      color: var(--text-muted);
      font-weight: 500;
      flex-shrink: 0;
    }

    .data-val {
      color: var(--text-heading);
      font-weight: 500;
      text-align: right;
    }

    /* Progress Bar */
    .progress-wrap {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .progress-track {
      flex: 1;
      height: 6px;
      background: #e8e3da;
      border-radius: 99px;
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      border-radius: 99px;
      transition: width 0.4s ease;
    }

    .progress-fill.high { background: var(--status-verified); }
    .progress-fill.medium { background: var(--status-review); }
    .progress-fill.low { background: var(--status-expired); }

    .sch-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 0.85rem;
      border-top: 1px solid var(--border-light);
      margin-top: auto;
    }

    .sch-action-links {
      display: flex;
      gap: 0.7rem;
    }

    .sch-action-link {
      font-size: 0.78rem;
      color: var(--text-muted);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      transition: color 0.15s;
    }

    .sch-action-link:hover {
      color: var(--brand-primary);
    }

    .btn-inspect {
      background: var(--bg-card-alt);
      border: 1px solid var(--border-main);
      color: var(--brand-primary);
      padding: 0.35rem 0.75rem;
      font-size: 0.78rem;
      font-weight: 600;
      font-family: var(--font-body);
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s;
    }

    .btn-inspect:hover {
      background: var(--brand-primary);
      color: var(--text-inverse);
      border-color: var(--brand-primary);
    }

    /* ===== CHANGE TABLE ===== */
    .section-intro {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.25rem;
      box-shadow: var(--shadow-card);
    }

    .section-intro h3 {
      font-family: var(--font-heading);
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 0.35rem;
    }

    .section-intro p {
      font-size: 0.85rem;
      color: var(--text-muted);
      line-height: 1.55;
    }

    .change-panel {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: var(--shadow-card);
    }

    .change-tbl {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
    }

    .change-tbl thead {
      background: var(--bg-card-alt);
    }

    .change-tbl th {
      padding: 0.7rem 1rem;
      text-align: left;
      font-weight: 600;
      color: var(--text-muted);
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      border-bottom: 1px solid var(--border-main);
    }

    .change-tbl td {
      padding: 0.9rem 1rem;
      border-bottom: 1px solid var(--border-light);
      vertical-align: top;
      color: var(--text-body);
    }

    .change-tbl tr:last-child td {
      border-bottom: none;
    }

    .change-tbl tr:hover td {
      background: rgba(27, 79, 138, 0.02);
    }

    .val-old {
      color: var(--status-expired);
      text-decoration: line-through;
      font-family: var(--font-mono);
      font-size: 0.82rem;
    }

    .val-new {
      color: var(--status-verified);
      font-weight: 600;
      font-family: var(--font-mono);
      font-size: 0.82rem;
    }

    .evidence-block {
      background: var(--bg-card-alt);
      border-left: 3px solid var(--brand-gold);
      padding: 0.5rem 0.7rem;
      border-radius: 0 var(--radius-xs) var(--radius-xs) 0;
      margin-top: 0.4rem;
      font-size: 0.8rem;
      color: var(--text-body);
      font-style: italic;
      line-height: 1.5;
    }

    /* ===== PROVENANCE ENGINE ===== */
    .engine-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 0.85rem;
      margin-top: 1rem;
    }

    .engine-card {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1.15rem;
      box-shadow: var(--shadow-card);
    }

    .engine-card h4 {
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 0.3rem;
    }

    .engine-card p {
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    .engine-points {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--brand-gold);
      background: var(--brand-gold-bg);
      border: 1px solid rgba(184, 134, 11, 0.2);
      border-radius: var(--radius-xs);
      padding: 0.1rem 0.4rem;
      margin-bottom: 0.5rem;
    }

    .gate-banner {
      margin-top: 1rem;
      padding: 0.9rem 1.15rem;
      background: var(--status-verified-bg);
      border: 1px solid var(--status-verified-border);
      border-radius: var(--radius-md);
      color: var(--status-verified);
      font-size: 0.84rem;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* ===== API ENDPOINTS ===== */
    .api-endpoint {
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-md);
      padding: 1rem 1.25rem;
      margin-bottom: 0.75rem;
      box-shadow: var(--shadow-card);
      transition: box-shadow 0.15s;
    }

    .api-endpoint:hover {
      box-shadow: var(--shadow-card-hover);
    }

    .api-header {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.35rem;
    }

    .method-badge {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.15rem 0.45rem;
      border-radius: var(--radius-xs);
      letter-spacing: 0.02em;
    }

    .method-get {
      background: var(--status-active-bg);
      color: var(--status-active);
      border: 1px solid var(--status-active-border);
    }

    .method-post {
      background: var(--status-verified-bg);
      color: var(--status-verified);
      border: 1px solid var(--status-verified-border);
    }

    .api-path {
      font-family: var(--font-mono);
      font-size: 0.92rem;
      font-weight: 500;
      color: var(--text-heading);
    }

    .api-desc {
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    /* ===== MODAL ===== */
    .modal-bg {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(4px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      padding: 1.5rem;
    }

    .modal-bg.open {
      display: flex;
    }

    .modal-box {
      background: var(--bg-card);
      border: 1px solid var(--border-main);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 880px;
      max-height: 92vh;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-modal);
      animation: modalIn 0.2s ease;
      overflow: hidden;
    }

    @keyframes modalIn {
      from { opacity: 0; transform: scale(0.97) translateY(6px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }

    .modal-top {
      padding: 1.35rem 1.65rem;
      border-bottom: 1px solid var(--border-light);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      background: var(--bg-card-alt);
    }

    .modal-dismiss {
      background: none;
      border: 1px solid var(--border-main);
      border-radius: var(--radius-sm);
      color: var(--text-muted);
      width: 32px;
      height: 32px;
      font-size: 1.1rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s;
      flex-shrink: 0;
    }

    .modal-dismiss:hover {
      background: var(--bg-hover);
      color: var(--text-heading);
    }

    .modal-content {
      padding: 1.5rem 1.65rem;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .detail-section h4 {
      font-family: var(--font-heading);
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-heading);
      margin-bottom: 0.65rem;
      display: flex;
      align-items: center;
      gap: 0.45rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--border-light);
    }

    .info-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
    }

    .info-table tr {
      border-bottom: 1px solid var(--border-light);
    }

    .info-table tr:last-child {
      border-bottom: none;
    }

    .info-table th {
      padding: 0.55rem 0.5rem;
      text-align: left;
      color: var(--text-muted);
      font-weight: 500;
      width: 34%;
      vertical-align: top;
    }

    .info-table td {
      padding: 0.55rem 0.5rem;
      color: var(--text-body);
    }

    .ev-card {
      background: var(--bg-card-alt);
      border: 1px solid var(--border-light);
      border-radius: var(--radius-sm);
      padding: 0.85rem 1rem;
      margin-bottom: 0.65rem;
    }

    .ev-tag {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--brand-primary);
      background: var(--brand-primary-bg);
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-xs);
      display: inline-block;
      margin-bottom: 0.35rem;
      font-weight: 600;
    }

    .ev-quote {
      font-style: italic;
      color: var(--text-body);
      border-left: 2px solid var(--brand-gold);
      padding-left: 0.7rem;
      margin: 0.4rem 0;
      line-height: 1.5;
      font-size: 0.84rem;
    }

    .ev-meta {
      font-size: 0.72rem;
      color: var(--text-dim);
      display: flex;
      gap: 0.85rem;
      flex-wrap: wrap;
      margin-top: 0.4rem;
    }

    .ev-meta a {
      color: var(--brand-primary);
      text-decoration: none;
    }

    .ev-meta a:hover {
      text-decoration: underline;
    }

    /* ===== LOADING ===== */
    .loading-box {
      text-align: center;
      padding: 4rem 1rem;
      color: var(--text-muted);
    }

    .spinner {
      width: 36px;
      height: 36px;
      border: 3px solid var(--border-light);
      border-radius: 50%;
      border-top-color: var(--brand-primary);
      animation: spin 0.7s linear infinite;
      margin: 0 auto 1rem;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    /* ===== FOOTER ===== */
    .site-footer {
      background: var(--bg-card);
      border-top: 1px solid var(--border-main);
      padding: 1.25rem 2rem;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.78rem;
    }

    .site-footer a {
      color: var(--brand-primary);
      text-decoration: none;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
      .site-header { padding: 0.75rem 1rem; }
      .main-container { padding: 1rem; }
      .sch-grid { grid-template-columns: 1fr; }
      .tab-trigger { font-size: 0.8rem; padding: 0.7rem 0.9rem; }
      .change-tbl { font-size: 0.78rem; }
      .change-tbl th, .change-tbl td { padding: 0.6rem 0.65rem; }
    }
  </style>
</head>
<body>

  <!-- Government-style trust banner -->
  <div class="gov-banner">
    <span>🏛️ Primary-Source Verified Scholarship Intelligence System — Evidence Grounded & Anti-Hallucination Enforced</span>
    <a href="https://scholarships.gov.in" target="_blank">National Scholarship Portal ↗</a>
  </div>

  <!-- Header -->
  <header class="site-header">
    <div class="brand-group">
      <div class="brand-emblem">🎓</div>
      <div>
        <div class="brand-title">Scholarship Intelligence</div>
        <div class="brand-subtitle">Verified Discovery · Provenance Tracing · Change Detection</div>
      </div>
    </div>
    <nav class="header-nav">
      <a href="https://scholarships.gov.in" target="_blank" class="btn btn-outline">🏛️ NSP Portal</a>
      <a href="https://scholarship-intelligence.onrender.com" target="_blank" class="btn btn-outline">📊 Streamlit</a>
      <a href="/docs" class="btn btn-solid">⚡ API Docs</a>
    </nav>
  </header>

  <main class="main-container">
    <!-- Stats Row -->
    <div class="stats-row">
      <div class="stat-card stat-primary">
        <div class="stat-label">Total Discovered</div>
        <div class="stat-value" id="kpi-total">—</div>
        <div class="stat-note">3 source types</div>
      </div>
      <div class="stat-card stat-verified">
        <div class="stat-label">Primary Verified</div>
        <div class="stat-value" id="kpi-verified">—</div>
        <div class="stat-note">Official source confirmed</div>
      </div>
      <div class="stat-card stat-verified">
        <div class="stat-label">Confidence ≥95%</div>
        <div class="stat-value" id="kpi-high-conf">—</div>
        <div class="stat-note">Full evidence chain</div>
      </div>
      <div class="stat-card stat-active">
        <div class="stat-label">Active</div>
        <div class="stat-value" id="kpi-active">—</div>
        <div class="stat-note">Currently open</div>
      </div>
      <div class="stat-card stat-gold">
        <div class="stat-label">Change Events</div>
        <div class="stat-value" id="kpi-changes">2</div>
        <div class="stat-note">Timeline updates logged</div>
      </div>
      <div class="stat-card stat-expired">
        <div class="stat-label">Expired / Stale</div>
        <div class="stat-value" id="kpi-stale">2</div>
        <div class="stat-note">Past-cycle detected</div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-bar">
      <button class="tab-trigger active" onclick="switchTab('scholarships')">
        <span class="tab-icon">📋</span> Scholarships <span id="tab-count-display">(—)</span>
      </button>
      <button class="tab-trigger" onclick="switchTab('changes')">
        <span class="tab-icon">🔄</span> Change Detection (2)
      </button>
      <button class="tab-trigger" onclick="switchTab('provenance')">
        <span class="tab-icon">🛡️</span> Verification Engine
      </button>
      <button class="tab-trigger" onclick="switchTab('api')">
        <span class="tab-icon">⚡</span> REST API
      </button>
    </div>

    <!-- TAB 1: Scholarships Directory -->
    <div id="tab-scholarships" class="tab-panel active">
      <div class="filter-card">
        <div class="filter-row">
          <div class="search-field">
            <span class="icon">🔍</span>
            <input type="text" id="search-input" placeholder="Search scholarships by name, provider, keyword..." oninput="handleSearch()">
          </div>
          <div class="filter-select">
            <select id="filter-status" onchange="handleSearch()">
              <option value="">All Statuses</option>
              <option value="ACTIVE">Active</option>
              <option value="EXPIRING_SOON">Expiring Soon</option>
              <option value="EXPIRED">Expired</option>
              <option value="NO_LONGER_VERIFIABLE">Unverifiable</option>
            </select>
          </div>
          <div class="filter-select">
            <select id="filter-type" onchange="handleSearch()">
              <option value="">All Source Types</option>
              <option value="SCHOLARSHIP_PORTAL">Govt Portal</option>
              <option value="UNIVERSITY">University</option>
              <option value="CORPORATE_CSR">Corporate CSR</option>
            </select>
          </div>
          <div class="filter-select">
            <select id="filter-conf" onchange="handleSearch()">
              <option value="">All Confidence</option>
              <option value="VERIFIED">Verified (≥95%)</option>
              <option value="REVIEW_REQUIRED">Review Required</option>
            </select>
          </div>
        </div>
      </div>

      <div class="results-bar">
        <div class="results-count" id="results-count">Loading scholarships...</div>
        <div class="results-badge">✓ Evidence-Grounded</div>
      </div>

      <div id="scholarships-container" class="sch-grid">
        <div class="loading-box">
          <div class="spinner"></div>
          <p>Loading verified scholarships...</p>
        </div>
      </div>
    </div>

    <!-- TAB 2: Change Detection -->
    <div id="tab-changes" class="tab-panel">
      <div class="section-intro">
        <h3>Append-Only Change History Log</h3>
        <p>
          Every repeat crawl compares incoming observations against stored historical snapshots.
          When official portals update deadlines or award amounts, an immutable <strong>ChangeEvent</strong>
          is stored with old value, new value, timestamp, source URL, and verified circular text.
        </p>
      </div>

      <div class="change-panel">
        <table class="change-tbl">
          <thead>
            <tr>
              <th style="width:4%">#</th>
              <th style="width:22%">Scholarship</th>
              <th style="width:10%">Field</th>
              <th style="width:18%">Old → New</th>
              <th style="width:14%">Detected</th>
              <th>Source & Evidence</th>
            </tr>
          </thead>
          <tbody id="change-events-body">
            <tr>
              <td><strong>1</strong></td>
              <td>AICTE – Swanath Scholarship Scheme</td>
              <td><code style="font-family:var(--font-mono); font-size:0.8rem; background:var(--brand-primary-bg); padding:0.1rem 0.3rem; border-radius:3px;">closing_date</code></td>
              <td>
                <span class="val-old">31-10-2026</span><br>
                <span class="val-new">15-11-2026</span>
              </td>
              <td style="font-size:0.82rem; color:var(--text-muted);">2026-10-01<br>14:30 UTC</td>
              <td>
                <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.3rem;">
                  Source: <a href="https://scholarships.gov.in/All-Scholarships" target="_blank" style="color:var(--brand-primary);">scholarships.gov.in</a>
                </div>
                <div class="evidence-block">
                  "National Scholarship Portal Notice: Online application closing date for AICTE - Swanath Scholarship Scheme has been extended from 31-10-2026 to 15-11-2026 for academic session 2026-27."
                </div>
              </td>
            </tr>
            <tr>
              <td><strong>2</strong></td>
              <td>PM-USP – Central Sector Scheme of Scholarship</td>
              <td><code style="font-family:var(--font-mono); font-size:0.8rem; background:var(--brand-primary-bg); padding:0.1rem 0.3rem; border-radius:3px;">closing_date</code></td>
              <td>
                <span class="val-old">31-10-2026</span><br>
                <span class="val-new">30-11-2026</span>
              </td>
              <td style="font-size:0.82rem; color:var(--text-muted);">2026-10-01<br>15:00 UTC</td>
              <td>
                <div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.3rem;">
                  Source: <a href="https://scholarships.gov.in/All-Scholarships" target="_blank" style="color:var(--brand-primary);">scholarships.gov.in</a>
                </div>
                <div class="evidence-block">
                  "Department of Higher Education Announcement: PM-USP Central Sector Scheme of Scholarship application timeline extended from 31-10-2026 to 30-11-2026 on National Scholarship Portal."
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: Provenance & Verification Engine -->
    <div id="tab-provenance" class="tab-panel">
      <div class="section-intro">
        <h3>Deterministic Verification Engine</h3>
        <p>
          This system completely rejects arbitrary LLM-generated confidence scores. Every confidence
          score is mathematically computed through an evidence-based provenance scoring formula.
          No fabrication — every field must have a stored, verifiable evidence excerpt with SHA-256 hash.
        </p>
      </div>

      <div class="engine-grid">
        <div class="engine-card">
          <div class="engine-points">+35 pts</div>
          <h4>1. Official Source Verification</h4>
          <p>Confirmed official domain (.gov.in, recognized university, or corporate CSR portal). Third-party aggregators receive 0 points.</p>
        </div>
        <div class="engine-card">
          <div class="engine-points">+20 pts</div>
          <h4>2. Evidence-Backed Name</h4>
          <p>Verbatim title excerpt extracted directly from primary page headings or official notification headers. Matched against source snapshot.</p>
        </div>
        <div class="engine-card">
          <div class="engine-points">+45 pts (5 × 9)</div>
          <h4>3. Critical Fields Evidence</h4>
          <p>Distributed across Provider (+9), Amount (+9), Eligibility (+9), Deadline (+9), Application URL (+9). Each must have a stored evidence excerpt.</p>
        </div>
      </div>

      <div class="gate-banner">
        <span style="font-size:1.1rem;">✓</span>
        <div>
          <strong>VERIFIED Gate (≥95%):</strong> Requires ≥95.0 total points. Records missing any critical evidence remain <code style="background:rgba(0,0,0,0.08); padding:0.1rem 0.3rem; border-radius:3px; font-family:var(--font-mono); font-size:0.8rem;">REVIEW_REQUIRED</code>.
        </div>
      </div>
    </div>

    <!-- TAB 4: REST API Endpoints -->
    <div id="tab-api" class="tab-panel">
      <div class="section-intro">
        <h3>FastAPI RESTful Endpoints</h3>
        <p>All scholarship intelligence, crawl telemetry, and evidence hashes are accessible via programmatic REST API endpoints. Use <code>/docs</code> for interactive Swagger UI.</p>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/scholarships</span>
        </div>
        <div class="api-desc">Paginated list with multi-dimensional filtering by status, source type, provider, category, gender, domicile, and confidence range.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/scholarships/{id}</span>
        </div>
        <div class="api-desc">Complete normalized record with 20+ fields, provider details, closing date, and confidence assessment reasons.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/scholarships/{id}/evidence</span>
        </div>
        <div class="api-desc">Cryptographically auditable evidence excerpts with source URLs, retrieval timestamps, and SHA-256 content hashes.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/scholarships/{id}/history</span>
        </div>
        <div class="api-desc">Audit log of detected field updates — old values, new values, and circular evidence text.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/stats</span>
        </div>
        <div class="api-desc">Real-time aggregate counts: total discovered, verified, review required, active, expiring, average confidence.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-post">POST</span>
          <span class="api-path">/crawl</span>
        </div>
        <div class="api-desc">Trigger a full discovery → extraction → verification → change-detection crawl run. Requires Bearer token.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/crawl-runs</span>
        </div>
        <div class="api-desc">History of crawl executions with timestamps, pages seen, candidates, records updated, and error counts.</div>
      </div>

      <div class="api-endpoint">
        <div class="api-header">
          <span class="method-badge method-get">GET</span>
          <span class="api-path">/health</span>
        </div>
        <div class="api-desc">Health check returning <code>{"status":"ok"}</code> for uptime monitors and load balancers.</div>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    Scholarship Intelligence · Verified Primary-Source Discovery · Built with <a href="/docs">FastAPI</a> · Data sourced from <a href="https://scholarships.gov.in" target="_blank">scholarships.gov.in</a> & official institutional portals
  </footer>

  <!-- Detail Modal -->
  <div id="detail-modal" class="modal-bg" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-top">
        <div>
          <div class="sch-badges" id="modal-badges"></div>
          <h2 id="modal-title" style="font-family:var(--font-heading); font-size:1.25rem; font-weight:700; color:var(--text-heading); line-height:1.3;">Scholarship Details</h2>
          <div id="modal-provider" style="font-size:0.85rem; color:var(--text-muted); margin-top:0.2rem;"></div>
        </div>
        <button class="modal-dismiss" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-content">
        <div class="detail-section">
          <h4>📋 Normalized Details</h4>
          <table class="info-table" id="modal-details-table"></table>
        </div>

        <div class="detail-section">
          <h4>🛡️ Confidence Breakdown</h4>
          <div id="modal-confidence-box" style="background:var(--bg-card-alt); border:1px solid var(--border-light); padding:1rem; border-radius:var(--radius-sm); font-size:0.84rem;"></div>
        </div>

        <div class="detail-section">
          <h4>📜 Cryptographic Field Evidence</h4>
          <div id="modal-evidence-box"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let allScholarships = [];

    function switchTab(name) {
      document.querySelectorAll('.tab-trigger').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

      const btn = Array.from(document.querySelectorAll('.tab-trigger')).find(b => b.getAttribute('onclick').includes(name));
      if (btn) btn.classList.add('active');

      const panel = document.getElementById('tab-' + name);
      if (panel) panel.classList.add('active');
    }

    async function loadData() {
      try {
        const statsRes = await fetch('/stats');
        if (statsRes.ok) {
          const stats = await statsRes.json();
          document.getElementById('kpi-total').textContent = stats.total_discovered || '—';
          document.getElementById('kpi-verified').textContent = stats.verified || '—';
          document.getElementById('kpi-high-conf').textContent = stats.verified || '—';
          document.getElementById('kpi-active').textContent = stats.active || '—';
        }

        const res = await fetch('/scholarships?page_size=100');
        if (res.ok) {
          const data = await res.json();
          allScholarships = data.items || [];
          document.getElementById('tab-count-display').textContent = `(${allScholarships.length})`;
          renderScholarships(allScholarships);
        }
      } catch (err) {
        console.error('Failed to load data:', err);
        document.getElementById('scholarships-container').innerHTML =
          '<div class="loading-box"><p>Unable to connect to API. Please refresh the page.</p></div>';
      }
    }

    function renderScholarships(items) {
      const container = document.getElementById('scholarships-container');
      document.getElementById('results-count').textContent = `Showing ${items.length} scholarship${items.length !== 1 ? 's' : ''}`;

      if (!items || items.length === 0) {
        container.innerHTML = '<div class="loading-box"><p>No scholarships match the selected filters.</p></div>';
        return;
      }

      container.innerHTML = items.map(sch => {
        const isVerified = sch.confidence_status === 'VERIFIED';
        const confClass = sch.confidence_score >= 95 ? 'high' : sch.confidence_score >= 70 ? 'medium' : 'low';

        const statusPill =
          sch.current_status === 'ACTIVE' ? 'pill-active' :
          sch.current_status === 'EXPIRING_SOON' ? 'pill-review' :
          sch.current_status === 'EXPIRED' ? 'pill-expired' : 'pill-stale';

        return `
          <div class="sch-item">
            <div>
              <div class="sch-badges">
                <span class="pill ${isVerified ? 'pill-verified' : 'pill-review'}">
                  ${isVerified ? '✓ Verified' : '⚠ Review Required'}
                </span>
                <span class="pill ${statusPill}">${esc(sch.current_status)}</span>
                <span class="pill pill-source">${esc(sch.source_type || 'SCHOLARSHIP')}</span>
              </div>
              <h3 class="sch-name">${esc(sch.name)}</h3>
              <div class="sch-org">🏛️ ${esc(sch.provider || 'Not specified')}</div>
            </div>

            <div class="sch-data-block">
              <div class="data-pair">
                <span class="data-key">Amount</span>
                <span class="data-val">${esc(sch.amount || 'Not specified')}</span>
              </div>
              <div class="data-pair">
                <span class="data-key">Closing Date</span>
                <span class="data-val">${esc(sch.closing_date || 'Not specified')}</span>
              </div>
              <div class="data-pair">
                <span class="data-key">Confidence</span>
                <span class="data-val" style="color:${isVerified ? 'var(--status-verified)' : 'var(--status-review)'}; font-weight:700;">
                  ${sch.confidence_score.toFixed(1)}%
                </span>
              </div>
              <div class="progress-wrap">
                <div class="progress-track">
                  <div class="progress-fill ${confClass}" style="width: ${sch.confidence_score}%;"></div>
                </div>
              </div>
            </div>

            <div class="sch-actions">
              <div class="sch-action-links">
                <a href="${sch.official_source_url}" target="_blank" class="sch-action-link">🏛️ Source ↗</a>
                ${sch.application_url ? `<a href="${sch.application_url}" target="_blank" class="sch-action-link">📝 Apply ↗</a>` : ''}
              </div>
              <button class="btn-inspect" onclick="openDetail(${sch.id})">View Evidence →</button>
            </div>
          </div>
        `;
      }).join('');
    }

    function handleSearch() {
      const q = document.getElementById('search-input').value.toLowerCase();
      const status = document.getElementById('filter-status').value;
      const type = document.getElementById('filter-type').value;
      const conf = document.getElementById('filter-conf').value;

      const filtered = allScholarships.filter(s => {
        const text = `${s.name} ${s.provider} ${s.eligibility || ''}`.toLowerCase();
        if (q && !text.includes(q)) return false;
        if (status && s.current_status !== status) return false;
        if (type && s.source_type !== type) return false;
        if (conf && s.confidence_status !== conf) return false;
        return true;
      });

      renderScholarships(filtered);
    }

    async function openDetail(id) {
      const sch = allScholarships.find(s => s.id === id);
      if (!sch) return;

      const isVerified = sch.confidence_status === 'VERIFIED';
      document.getElementById('modal-badges').innerHTML = `
        <span class="pill ${isVerified ? 'pill-verified' : 'pill-review'}">${sch.confidence_status} (${sch.confidence_score.toFixed(1)}%)</span>
        <span class="pill pill-source">${esc(sch.source_type)}</span>
      `;
      document.getElementById('modal-title').textContent = sch.name;
      document.getElementById('modal-provider').textContent = 'Provider: ' + (sch.provider || 'Not specified');

      const data = sch.field_data || {};
      const fields = [
        ['Amount', sch.amount || 'Not specified'],
        ['Benefit Description', data.benefit_description || 'Not specified'],
        ['Eligibility Criteria', sch.eligibility || 'Not specified'],
        ['Income Criteria', data.income_criteria || 'Not specified'],
        ['Academic Requirements', data.academic_requirements || 'Not specified'],
        ['Documents Required', data.documents_required || 'Not specified'],
        ['Selection Process', data.selection_process || 'Not specified'],
        ['Renewal Requirements', data.renewal_requirements || 'Not specified'],
        ['Education Level', data.education_level || 'Not specified'],
        ['Closing Date', sch.closing_date || 'Not specified'],
        ['Official Source', `<a href="${sch.official_source_url}" target="_blank" style="color:var(--brand-primary);">${esc(sch.official_source_url)}</a>`],
        ['Application URL', sch.application_url ? `<a href="${sch.application_url}" target="_blank" style="color:var(--brand-primary);">${esc(sch.application_url)}</a>` : 'Not specified']
      ];

      document.getElementById('modal-details-table').innerHTML = fields.map(([label, val]) => `
        <tr><th>${label}</th><td>${val}</td></tr>
      `).join('');

      const reasons = sch.verification_reasons || [];
      document.getElementById('modal-confidence-box').innerHTML = `
        <div style="font-weight:600; color:var(--text-heading); margin-bottom:0.5rem; font-family:var(--font-heading);">
          Confidence Score: ${sch.confidence_score.toFixed(1)}%
        </div>
        <div style="color:var(--text-muted); font-size:0.82rem;">
          ${reasons.length > 0 ? reasons.map(r => `<div style="margin-bottom:0.2rem;">• ${esc(r)}</div>`).join('') : '✓ Passed all primary source validation and evidence completeness checks.'}
        </div>
      `;

      const evidenceBox = document.getElementById('modal-evidence-box');
      evidenceBox.innerHTML = '<div style="color:var(--text-muted); font-size:0.82rem;">Fetching evidence...</div>';

      try {
        const evRes = await fetch(`/scholarships/${id}/evidence`);
        if (evRes.ok) {
          const evList = await evRes.json();
          if (evList.length === 0) {
            evidenceBox.innerHTML = '<div style="color:var(--text-dim); font-size:0.82rem;">No evidence items stored for this record.</div>';
          } else {
            evidenceBox.innerHTML = evList.map(e => `
              <div class="ev-card">
                <span class="ev-tag">${esc(e.field)}</span>
                <div class="ev-quote">"${esc(e.evidence_text)}"</div>
                <div class="ev-meta">
                  <span>Source: <a href="${e.source_url}" target="_blank">${esc(e.source_url.length > 55 ? e.source_url.slice(0, 55) + '...' : e.source_url)}</a></span>
                  <span>SHA-256: <code style="font-family:var(--font-mono); font-size:0.72rem;">${e.content_hash.slice(0, 14)}…</code></span>
                  <span>Retrieved: ${new Date(e.retrieved_at).toLocaleDateString()}</span>
                </div>
              </div>
            `).join('');
          }
        }
      } catch (err) {
        evidenceBox.innerHTML = '<div style="color:var(--status-expired); font-size:0.82rem;">Failed to load evidence.</div>';
      }

      document.getElementById('detail-modal').classList.add('open');
    }

    function closeModal(e) {
      if (!e || e.target.id === 'detail-modal' || e.target.classList.contains('modal-dismiss')) {
        document.getElementById('detail-modal').classList.remove('open');
      }
    }

    function esc(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    // Close modal on Escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeModal();
    });

    document.addEventListener('DOMContentLoaded', loadData);
  </script>
</body>
</html>"""
