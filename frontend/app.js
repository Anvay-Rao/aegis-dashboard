const API_BASE = "http://127.0.0.1:8000";

async function fetchSecure(endpoint) {
    const token = localStorage.getItem("access_token");
    
    if (!token) {
        window.location.href = "index.html";
        return null;
    }

    try {
        console.log("Fetching dashboard...");
        const res = await fetch(`http://127.0.0.1:8000/dashboard`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        
        if (res.status === 401) {
            window.location.href = "index.html";
            return null;
        }
        
        if (!res.ok) {
            console.warn("API returned non-200 status:", res.status);
            return null;
        }

        const data = await res.json();
        console.log("API response:", data);
        return data;
    } catch (err) {
        console.warn("API Fetch Failed:", err);
        showApiErrorWarning();
        return null;
    }
}

function showApiErrorWarning() {
    const header = document.querySelector("header");
    if (header && !document.getElementById("api-error")) {
        const err = document.createElement("div");
        err.id = "api-error";
        err.className = "bg-error text-on-error px-4 py-1 flex items-center gap-2 fixed top-0 w-full z-[100]";
        err.innerHTML = `<span class="material-symbols-outlined text-sm">warning</span> <span>API Offline - Connection Lost</span>`;
        header.prepend(err);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    const path = window.location.pathname;
    if (path.endsWith("index.html") || path.endsWith("/") || path === "") {
        return;
    }

    // Step 5: Add Interactivity
    bindNavigation();

    // Initial load
    const payload = await fetchSecure("/dashboard");
    if (payload) {
        renderAll(path, payload);
    }
    
    // Step 6: Auto Refresh (Exactly 3s)
    setInterval(async () => {
        const freshData = await fetchSecure("/dashboard");
        if (freshData) {
            renderAll(path, freshData);
            
            // Clear API error warning if it exists
            const err = document.getElementById("api-error");
            if (err) err.remove();
        }
    }, 3000);
});

function bindNavigation() {
    // Top Tabs
    const navLinks = document.querySelectorAll("nav a");
    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const text = link.innerText.toUpperCase();
            if (text.includes("FORENSIC")) window.location.href = "dashboard.html";
            else if (text.includes("SCHEMA")) window.location.href = "schema.html";
            else if (text.includes("ASSET")) window.location.href = "assets.html";
            else if (text.includes("HEATMAP")) window.location.href = "heatmap.html";
        });
    });

    // Buttons (Side Nav & Layouts)
    const interactables = document.querySelectorAll("button, a");
    interactables.forEach(el => {
        const text = (el.innerText || "").toUpperCase();
        
        if (text.includes("LOGOUT") || text.includes("EXIT")) {
            el.addEventListener("click", (e) => {
                e.preventDefault();
                console.log("Logging out...");
                localStorage.removeItem("access_token");
                window.location.href = "index.html";
            });
        }
        else if (text.includes("TERM") && text !== "TERMINAL INFO") {
            el.addEventListener("click", (e) => {
                e.preventDefault();
                window.location.href = "terminal.html";
            });
        }
        else if (text.includes("INITIATE BREACH")) {
            el.addEventListener("click", (e) => {
                e.preventDefault();
                console.log("BREACH INITIATED!");
                alert("BREACH PROTOCOL INITIATED.");
            });
        }
    });
}

function renderAll(path, data) {
    if (!data) return;
    
    // Default Metadata rendering over all pages
    renderMetadata(data);

    if (path.includes("dashboard.html")) {
        console.log("Rendering section... (Main Dashboard)");
        renderMainDashboard(data);
    } else if (path.includes("assets.html")) {
        console.log("Rendering section... (Assets)");
        renderAssets(data);
    } else if (path.includes("schema.html")) {
        console.log("Rendering section... (Schema)");
        renderSchema(data);
    } else if (path.includes("heatmap.html")) {
        console.log("Rendering section... (Heatmap)");
        renderHeatmap(data);
    } else if (path.includes("terminal.html")) {
        console.log("Rendering section... (Terminal)");
        renderTerminal(data);
    }
}

function renderMetadata(data) {
    const activeNodesEl = document.querySelector(".text-primary-container.px-2") || 
                          document.querySelector("div:contains('ACTIVE_NODES')");
    if (activeNodesEl && data.nodes) {
        activeNodesEl.innerHTML = `ACTIVE_NODES: ${data.nodes.length}`;
    }
}

function renderMainDashboard(data) {
    // A. NODE MAP
    const gridEl = document.querySelector(".grid-cols-25") || 
                   document.querySelector(".forensic-node-map") || 
                   document.querySelector(".grid");
                   
    if (gridEl) {
        gridEl.innerHTML = "";
        data.nodes.forEach(node => {
            const div = document.createElement("div");
            // Hover Effects
            div.title = `ID: ${node.id} | Status: ${node.is_infected ? 'INFECTED' : node.conflict_detected ? 'CONFLICT' : 'NORMAL'}`;
            
            if (node.is_infected) {
                div.className = "w-1.5 h-1.5 bg-error pulse-red rounded-full cursor-help hover:scale-150 transition-transform";
            } else if (node.conflict_detected) {
                div.className = "w-[6px] h-[6px] bg-secondary animate-pulse rounded-full cursor-help hover:scale-150 transition-transform";
            } else {
                div.className = "w-1.5 h-1.5 bg-primary-container/40 rounded-full shadow-[0_0_4px_#00FBFB] cursor-help hover:scale-150 transition-transform hover:bg-[#00FBFB]";
            }
            gridEl.appendChild(div);
        });
    } else {
        console.warn("Missing element:", ".grid-cols-25 or .forensic-node-map");
    }

    // Call child renderers inline for the components included on dashboard
    renderHeatmap(data);
    renderSchema(data);
    renderAssetsFallback(data);
    renderTerminal(data);
}

// Minimal fallback for dashboard.html which only has a small asset preview
function renderAssetsFallback(data) {
    const tbody = document.querySelector("tbody");
    if (!tbody) {
        console.warn("Missing element:", "tbody (Assets table fallback)");
        return;
    }
    
    tbody.innerHTML = "";
    data.nodes.forEach((node, i) => {
        if (i > 4) return; // Dashboard only shows ~5 elements

        const tr = document.createElement("tr");
        let trClass = "hover:bg-primary-container/5 transition-colors cursor-crosshair group";
        let statusBadge = `<span class="px-1 border border-primary-container text-[8px] text-primary-container uppercase">Operational</span>`;
        
        if (node.is_infected) {
            trClass = "bg-error/10 hover:bg-error/20 transition-colors cursor-crosshair group";
            statusBadge = `<span class="px-1 border border-error text-[8px] text-error uppercase">Breach</span>`;
        } else if (node.conflict_detected) {
            trClass = "bg-secondary/10 hover:bg-secondary/20 transition-colors cursor-crosshair group";
            statusBadge = `<span class="px-1 border border-secondary text-[8px] text-secondary uppercase">Conflict</span>`;
        }

        tr.className = trClass;
        tr.innerHTML = `
            <td class="p-3 ${node.is_infected ? 'text-error' : 'text-primary-container'} font-bold">${node.id}</td>
            <td class="p-3 text-outline truncate max-w-[150px]">${node.encoded_ua}</td>
            <td class="p-3 text-white">${node.decoded_serial}</td>
            <td class="p-3 text-right">${statusBadge}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderAssets(data) {
    const tbody = document.querySelector("tbody");
    if (!tbody) {
        console.warn("Missing element:", "tbody (Assets table main page)");
        return;
    }
    
    tbody.innerHTML = "";
    data.nodes.forEach((node, i) => {
        if (i > 50) return;

        const tr = document.createElement("tr");
        let trClass = "hover:bg-surface-container-highest transition-colors group";
        let statusBadge = `<span class="flex items-center gap-2 text-[#00FBFB]"><span class="w-1.5 h-1.5 bg-[#00FBFB] glow-cyan"></span>OPERATIONAL</span>`;
        let statusClass = "text-[#00FBFB]";
        
        if (node.is_infected) {
            statusBadge = `<span class="flex items-center gap-2 text-error"><span class="w-1.5 h-1.5 bg-error"></span>BREACH</span>`;
            statusClass = "text-error";
            trClass = "hover:bg-error/10 transition-colors group";
        } else if (node.conflict_detected) {
            statusBadge = `<span class="flex items-center gap-2 text-secondary"><span class="w-1.5 h-1.5 bg-secondary animate-pulse"></span>HIGH_LOAD</span>`;
            statusClass = "text-secondary";
            trClass = "hover:bg-secondary/10 transition-colors group";
        }

        tr.className = trClass;
        tr.innerHTML = `
            <td class="px-6 py-4 ${statusClass}">${node.id}</td>
            <td class="px-6 py-4 text-on-surface">${node.decoded_serial}</td>
            <td class="px-6 py-4 text-outline">${node.encoded_ua}</td>
            <td class="px-6 py-4">
                <div class="w-24 h-1 bg-surface-container-highest relative">
                    <div class="absolute left-0 top-0 h-full ${statusClass.replace('text-', 'bg-')}" style="width: ${Math.floor(Math.random() * 60 + 20)}%;"></div>
                </div>
            </td>
            <td class="px-6 py-4">${statusBadge}</td>
            <td class="px-6 py-4">
                <button class="opacity-0 group-hover:opacity-100 transition-opacity text-[#00FBFB] underline decoration-dotted">DIAGNOSTIC</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderSchema(data) {
    const schemaBlocks = document.querySelectorAll(".flex-grow.bg-black.p-4 > div");
    
    if (schemaBlocks.length > 0) {
        // Find trailing text lines, animate new ones mimicking schema sync
        const lastBlock = schemaBlocks[schemaBlocks.length - 2]; 
        if(lastBlock && data.schema_engine) {
            lastBlock.innerText = `[${new Date().toLocaleTimeString()}] SYSTEM_SYNC: Switching to L_V${data.schema_engine.current_version} column`;
            lastBlock.className = "text-white mb-1 transition-colors duration-200";
        }
        
        // Find general titles
        const titles = document.querySelectorAll(".text-secondary, .text-primary-container");
        titles.forEach(el => {
            if (el.innerText.includes("L_V")) {
                el.innerText = `L_V${data.schema_engine.current_version}_ACTIVE`;
            }
        });
    } else {
         console.warn("Missing element:", "Schema terminal text blocks");
    }
}

function renderHeatmap(data) {
    // Heatmap inline vertical bar chart
    const chartContainer = document.querySelector(".w-full.h-48.border-l") || 
                           document.querySelector(".h-80.w-full.border-l") ||
                           document.querySelector(".flex-grow.p-4.relative.flex.items-end .border-l") ||
                           document.querySelector(".flex-grow.relative.flex.items-end .border-l");
                           
    if (chartContainer && data.heatmap_data && data.heatmap_data.avg_latency.length > 0) {
        chartContainer.innerHTML = "";
        const maxLat = Math.max(...data.heatmap_data.avg_latency, 100);
        data.heatmap_data.avg_latency.slice(-20).forEach(lat => {
            const pct = Math.min((lat / maxLat) * 100, 100);
            const div = document.createElement("div");
            
            if (lat > 200) {
                div.className = `w-4 bg-secondary/30 h-[${pct}%] border-t border-secondary relative group transition-all duration-300`;
                div.innerHTML = `<div class="hidden group-hover:block absolute -top-8 left-1/2 -translate-x-1/2 bg-secondary text-on-secondary-fixed text-[8px] px-1 whitespace-nowrap">${lat.toFixed(0)}ms (ANOMALY)</div>`;
            } else {
                div.className = `w-4 bg-primary-container/20 h-[${pct}%] border-t border-primary-container transition-all duration-300`;
            }
            chartContainer.appendChild(div);
        });
    } else if (window.location.pathname.includes("heatmap") || window.location.pathname.includes("dashboard")) {
        console.warn("Missing element:", "Heatmap chart container (.border-l)");
    }

    // Advanced analytics readouts
    const threatDisplay = document.querySelector(".text-2xl.font-black.text-primary-fixed.mb-4, .text-2xl.font-black");
    if (threatDisplay && threatDisplay.innerText.includes("%")) {
        const infectionRate = ((data.metadata.active_threats / data.nodes.length) * 100).toFixed(1);
        threatDisplay.innerText = `${infectionRate}%`;
        const bar = document.querySelector('.bg-primary-fixed');
        if (bar) bar.style.width = `${infectionRate}%`;
    }
}

function renderTerminal(data) {
    const list = document.querySelector(".p-6.flex-grow.font-mono.flex.flex-col") ||
                 document.querySelector(".flex-grow.bg-black.p-4.font-mono") ||
                 document.getElementById("live-logs-container")?.parentElement ||
                 document.querySelector("div.font-mono.text-xs") ||
                 document.querySelector(".p-6.flex-grow.font-mono.flex.flex-col, .font-mono.text-xs, #live-logs-container");
                 
    if (!list) {
        console.warn("Missing element:", ".p-6.flex-grow.font-mono.flex.flex-col (Terminal UI)");
        return;
    }
    
    let liveLogContainer = document.getElementById("live-logs-container");
    if (!liveLogContainer) {
        liveLogContainer = document.createElement("div");
        liveLogContainer.id = "live-logs-container";
        liveLogContainer.className = "mt-4 space-y-1 opacity-90 text-[10px] md:text-sm overflow-y-auto cyber-scrollbar max-h-[600px] bg-black/50 p-4 border border-outline-variant/20";
        list.appendChild(liveLogContainer);
    }
    
    if (data.live_terminal_logs && data.live_terminal_logs.length > 0) {
        liveLogContainer.innerHTML = "";
        data.live_terminal_logs.slice().reverse().forEach(log => {
            const p = document.createElement("p");
            if (log.includes("HTTP 5") || log.includes("error")) {
                p.className = "text-error font-bold";
            } else if (log.includes("HTTP 4")) {
                p.className = "text-secondary";
            } else {
                p.className = "text-primary-fixed-dim";
            }
            p.innerText = `> ${log}`;
            liveLogContainer.appendChild(p);
        });
    }
}
