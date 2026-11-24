
import { useState } from "react";
import Editor from "@monaco-editor/react";
import {
  Activity, BarChart3, BookOpen, Code2, LayoutDashboard,
  Settings, History, Zap, Clock, HardDrive, Upload,
  Play, Trash2, Copy, Check, Search, Bell, ChevronDown,
  Lightbulb, AlertTriangle, Menu, X, FileCode2, Moon,
  Sparkles, Gauge, Cpu, ArrowUpRight
} from "lucide-react";
import { analyzeCode } from "./api";
import "./App.css";

const languages = [
  "python", "javascript", "typescript", "java",
  "cpp", "c", "go", "php", "ruby", "csharp"
];

const languageLabels = {
  python: "Python", javascript: "JavaScript",
  typescript: "TypeScript", java: "Java",
  cpp: "C++", c: "C", go: "Go",
  php: "PHP", ruby: "Ruby", csharp: "C#"
};

const sampleCode = {
  python: `def find_pairs(numbers):
    pairs = []

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == 10:
                pairs.append((numbers[i], numbers[j]))

    return pairs

result = find_pairs([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(result)`,
  javascript: `function findPairs(numbers) {
  const pairs = [];

  for (let i = 0; i < numbers.length; i++) {
    for (let j = i + 1; j < numbers.length; j++) {
      if (numbers[i] + numbers[j] === 10) {
        pairs.push([numbers[i], numbers[j]]);
      }
    }
  }

  return pairs;
}

console.log(findPairs([1, 2, 3, 4, 5, 6]));`,
  java: `public class Main {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5, 6};

        for (int i = 0; i < numbers.length; i++) {
            for (int j = i + 1; j < numbers.length; j++) {
                System.out.println(numbers[i] + numbers[j]);
            }
        }
    }
}`
};

function StatCard({ title, value, subtitle, icon: Icon, color, trend }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <div className={`stat-icon ${color}`}><Icon size={21} /></div>
        <span className="stat-trend"><ArrowUpRight size={14}/>{trend}</span>
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-title">{title}</div>
      <div className="stat-subtitle">{subtitle}</div>
    </div>
  );
}

function ResultCard({ icon: Icon, title, value, description, color }) {
  return (
    <div className="result-card">
      <div className={`result-icon ${color}`}><Icon size={20}/></div>
      <div className="result-label">{title}</div>
      <div className="result-value">{value || "—"}</div>
      <div className="result-description">{description || "Run an analysis to see results."}</div>
    </div>
  );
}

export default function App() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(sampleCode.python);
  const [activePage, setActivePage] = useState("Dashboard");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mobileMenu, setMobileMenu] = useState(false);
  const [copied, setCopied] = useState(false);
  const [history, setHistory] = useState([]);

  const changeLanguage = (value) => {
    setLanguage(value);
    setCode(sampleCode[value] || "");
    setResult(null);
    setError("");
  };

  const runAnalysis = async () => {
    if (!code.trim()) {
      setError("Please enter or upload some code before analyzing.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeCode(code, language);
      setResult(data);
      setHistory((previous) => [
        {
          language: languageLabels[language],
          time: new Date().toLocaleTimeString(),
          complexity: data.time_complexity || "Unknown"
        },
        ...previous
      ]);
    } catch (err) {
      setError(err.message || "Analysis failed. Please check your backend server.");
    } finally {
      setLoading(false);
    }
  };

  const clearCode = () => {
    setCode("");
    setResult(null);
    setError("");
  };

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      setError("Could not copy code. Please copy it manually.");
    }
  };

  const uploadFile = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const extensionMap = {
      py: "python", js: "javascript", ts: "typescript",
      java: "java", cpp: "cpp", c: "c",
      go: "go", php: "php", rb: "ruby", cs: "csharp"
    };

    const extension = file.name.split(".").pop().toLowerCase();
    const detected = extensionMap[extension];

    if (detected) setLanguage(detected);

    const reader = new FileReader();
    reader.onload = () => {
      setCode(String(reader.result || ""));
      setResult(null);
      setError("");
    };
    reader.readAsText(file);
    event.target.value = "";
  };

  const navigation = [
    { name: "Dashboard", icon: LayoutDashboard },
    { name: "Code Analyzer", icon: Code2 },
    { name: "Analysis History", icon: History },
    { name: "Documentation", icon: BookOpen },
    { name: "Settings", icon: Settings }
  ];

  return (
    <div className="app-shell">
      {mobileMenu && <div className="mobile-overlay" onClick={() => setMobileMenu(false)} />}

      <aside className={`sidebar ${mobileMenu ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-logo"><Code2 size={25}/></div>
          <div>
            <div className="brand-name">CodeXpert<span> AI</span></div>
            <div className="brand-caption">CODE INTELLIGENCE</div>
          </div>
          <button className="mobile-close" onClick={() => setMobileMenu(false)}><X/></button>
        </div>

        <div className="sidebar-section">WORKSPACE</div>
        <nav className="nav-list">
          {navigation.map(({ name, icon: Icon }) => (
            <button
              key={name}
              className={`nav-item ${activePage === name ? "active" : ""}`}
              onClick={() => {
                setActivePage(name);
                setMobileMenu(false);
              }}
            >
              <Icon size={19}/>
              <span>{name}</span>
              {name === "Code Analyzer" && <span className="nav-new">NEW</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon"><Sparkles size={19}/></div>
            <h4>Code smarter with AI</h4>
            <p>Understand your code and discover better ways to optimize it.</p>
            <button onClick={() => setActivePage("Code Analyzer")}>Start analyzing <ArrowUpRight size={15}/></button>
          </div>
          <div className="profile">
            <div className="avatar">CX</div>
            <div className="profile-info">
              <strong>Developer</strong>
              <span>Free workspace</span>
            </div>
            <Settings size={17} className="profile-settings"/>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <button className="menu-toggle" onClick={() => setMobileMenu(true)}><Menu/></button>
            <div className="breadcrumb">Workspace <span>/</span> <strong>{activePage}</strong></div>
          </div>
          <div className="topbar-right">
            <div className="system-status"><span/> System ready</div>
            <button className="top-icon" title="Dark theme"><Moon size={19}/></button>
            <button className="top-icon notification" title="Notifications"><Bell size={19}/></button>
            <div className="top-avatar">CX</div>
          </div>
        </header>

        <div className="page-container">
          {activePage === "Dashboard" || activePage === "Code Analyzer" ? (
            <>
              <section className="welcome-section">
                <div>
                  <div className="eyebrow"><Sparkles size={15}/> INTELLIGENT CODE ANALYSIS</div>
                  <h1>{activePage === "Dashboard" ? <>Welcome to <span>CodeXpert AI</span></> : <>Code <span>Analyzer</span></>}</h1>
                  <p>Understand your code. Analyze complexity. Build smarter algorithms.</p>
                </div>
                <div className="welcome-decoration"><Code2 size={65}/></div>
              </section>

              <section className="stats-grid">
                <StatCard title="Codes Analyzed" value={history.length} subtitle="This session" icon={FileCode2} color="purple" trend="Live"/>
                <StatCard title="Average Efficiency" value={result?.efficiency != null ? `${result.efficiency}/100` : "—"} subtitle="Based on analysis" icon={Gauge} color="cyan" trend="Score"/>
                <StatCard title="Current Language" value={languageLabels[language]} subtitle="Selected language" icon={Cpu} color="green" trend="Active"/>
                <StatCard title="Latest Complexity" value={result?.time_complexity || "—"} subtitle="Most recent analysis" icon={Activity} color="orange" trend="Latest"/>
              </section>

              <section className="section-heading">
                <div>
                  <h2>Code Analysis Studio</h2>
                  <p>Paste your source code or upload a file to begin.</p>
                </div>
                <div className="editor-status"><span/> Editor ready</div>
              </section>

              <section className="editor-card">
                <div className="editor-toolbar">
                  <div className="editor-title"><div className="editor-dot"/> <span>Code Editor</span><span className="editor-file">main.{language === "python" ? "py" : language === "javascript" ? "js" : language}</span></div>
                  <div className="editor-actions">
                    <select value={language} onChange={(e) => changeLanguage(e.target.value)} aria-label="Programming language">
                      {languages.map((lang) => <option value={lang} key={lang}>{languageLabels[lang]}</option>)}
                    </select>
                    <label className="tool-button upload-button"><Upload size={15}/> Upload<input type="file" accept=".py,.js,.ts,.java,.cpp,.c,.go,.php,.rb,.cs,.txt" onChange={uploadFile}/></label>
                    <button className="tool-button" onClick={copyCode}>{copied ? <Check size={15}/> : <Copy size={15}/>} {copied ? "Copied" : "Copy"}</button>
                    <button className="tool-button clear-button" onClick={clearCode}><Trash2 size={15}/> Clear</button>
                  </div>
                </div>

                <div className="editor-wrapper">
                  <Editor
                    height="390px"
                    language={language === "cpp" ? "cpp" : language === "csharp" ? "csharp" : language}
                    theme="vs-dark"
                    value={code}
                    onChange={(value) => setCode(value || "")}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 14,
                      lineNumbers: "on",
                      roundedSelection: true,
                      scrollBeyondLastLine: false,
                      automaticLayout: true,
                      padding: { top: 18 },
                      tabSize: 4,
                      wordWrap: "on"
                    }}
                  />
                </div>

                <div className="editor-footer">
                  <div><span className="footer-language"><Code2 size={14}/> {languageLabels[language]}</span><span>{code.split("\n").length} lines</span><span>{code.length} characters</span></div>
                  <span>Static analysis · No code execution</span>
                </div>
              </section>

              {error && <div className="error-message"><AlertTriangle size={18}/>{error}</div>}

              <div className="analyze-row">
                <div className="analyze-hint"><Lightbulb size={17}/> Analysis is an estimate, not a runtime benchmark.</div>
                <button className="analyze-button" onClick={runAnalysis} disabled={loading}>
                  {loading ? <span className="spinner"/> : <Play size={17} fill="currentColor"/>}
                  {loading ? "Analyzing code..." : "Analyze Code"}
                  {!loading && <ArrowUpRight size={17}/>}
                </button>
              </div>

              <section className="section-heading results-heading">
                <div><h2>Analysis Results</h2><p>Complexity insights and performance recommendations.</p></div>
                {result && <span className="result-ready"><Check size={14}/> Analysis complete</span>}
              </section>

            <section className="results-grid">
             <ResultCard
               icon={Clock}
               title="TIME COMPLEXITY"
               value={result?.time_complexity}
               description={result?.time_explanation}
               color="purple"
              />

               <ResultCard
                icon={Clock}
                title="BEST-CASE TIME"
               value={result?.best_case_time_complexity || "—"}
               description="Estimated complexity in the most favorable case."
               color="green"
              />

              <ResultCard
               icon={Clock}
               title="WORST-CASE TIME"
               value={result?.worst_case_time_complexity || "—"}
               description="Estimated complexity in the least favorable case."
               color="purple"
              />

              <ResultCard
                icon={HardDrive}
                title="SPACE COMPLEXITY"
                value={result?.space_complexity}
                description={result?.space_explanation}
                color="cyan"
              />

             <ResultCard
                icon={Gauge}
                title="EFFICIENCY SCORE"
                value={result?.efficiency != null ? `${result.efficiency}/100` : "—"}
                description={result?.efficiency_explanation || "Efficiency score based on estimated complexity."}
                color="green"
              />
            </section>

              {result && (
                <>
                  <section className="insights-grid">
                    <div className="insight-card">
                      <div className="insight-heading"><AlertTriangle size={18}/><h3>Performance Bottlenecks</h3></div>
                      {result.bottlenecks?.length ? result.bottlenecks.map((item, i) => <div className="insight-item" key={i}>{typeof item === "string" ? item : item.message}</div>) : <p className="empty-insight">No bottlenecks reported by the analyzer.</p>}
                    </div>
                    <div className="insight-card">
                      <div className="insight-heading suggestion-heading"><Lightbulb size={18}/><h3>Optimization Suggestions</h3></div>
                      {result.suggestions?.length ? result.suggestions.map((item, i) => <div className="insight-item" key={i}>{typeof item === "string" ? item : item.message}</div>) : <p className="empty-insight">No suggestions reported by the analyzer.</p>}
                    </div>
                  </section>
                  <div className="confidence-note">
                    <Activity size={16}/>
                    <span>Analysis confidence: <strong>{result.confidence || "Not provided"}</strong>. Static analysis may not resolve every runtime-dependent behavior.</span>
                  </div>
                </>
              )}
            </>
          ) : activePage === "Analysis History" ? (
            <section className="simple-page">
              <div className="eyebrow"><History size={15}/> YOUR WORKSPACE</div>
              <h1>Analysis <span>History</span></h1>
              <p className="simple-description">Your recent analyses from this session.</p>
              {history.length ? history.map((item, i) => (
                <div className="history-row" key={i}>
                  <FileCode2 size={20}/><strong>{item.language}</strong><span>{item.complexity}</span><small>{item.time}</small>
                </div>
              )) : <div className="empty-state"><History size={36}/><h3>No analysis yet</h3><p>Your completed analyses will appear here.</p><button onClick={() => setActivePage("Code Analyzer")}>Open Code Analyzer</button></div>}
            </section>
          ) : activePage === "Documentation" ? (
            <section className="simple-page">
              <div className="eyebrow"><BookOpen size={15}/> HELP CENTER</div>
              <h1>CodeXpert <span>Documentation</span></h1>
              <p className="simple-description">Learn how to use the code complexity analyzer.</p>
              <div className="doc-card"><h3>1. Select a language</h3><p>Choose one of the supported programming languages from the editor toolbar.</p></div>
              <div className="doc-card"><h3>2. Add your code</h3><p>Paste code into the editor or upload a supported source file.</p></div>
              <div className="doc-card"><h3>3. Analyze your code</h3><p>Click Analyze Code to send your source to the backend analysis API.</p></div>
              <div className="doc-card"><h3>4. Understand the results</h3><p>Review estimated time complexity, auxiliary space complexity, efficiency score and suggestions.</p></div>
            </section>
          ) : (
            <section className="simple-page">
              <div className="eyebrow"><Settings size={15}/> PREFERENCES</div>
              <h1>Workspace <span>Settings</span></h1>
              <p className="simple-description">CodeXpert AI workspace information.</p>
              <div className="doc-card"><h3>Appearance</h3><p>Current interface: Dark theme.</p></div>
              <div className="doc-card"><h3>Analysis mode</h3><p>Static code analysis. Source code is sent to your configured local backend.</p></div>
              <div className="doc-card"><h3>Supported languages</h3><p>{languages.map(l => languageLabels[l]).join(", ")}</p></div>
            </section>
          )}

          <footer className="page-footer">
            <span>© 2026 CodeXpert AI</span>
            <span>Built for smarter code analysis <Sparkles size={13}/></span>
          </footer>
        </div>
      </main>
    </div>
  );
}
