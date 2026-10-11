
const $ = id => document.getElementById(id);
let initial = {};

async function poll(){
  let d;
  try { d = await (await fetch("/status", {cache:"no-store"})).json(); }
  catch(e){ return; }

  const scr = $("screen");
  scr.classList.toggle("alarm", d.locked);
  $("screenMsg").textContent = d.screen;
  $("screenNonce").textContent = d.locked
    ? `Out of service — auto-recovers in ${d.lock_remaining}s`
    : "Session code: " + d.nonce;

  $("dotArmed").className = "dot" + (d.armed ? " on" : "");
  $("txtArmed").textContent = d.armed ? "ON" : "OFF";

  $("dotMon").className = "dot" + (d.monitor_on ? " on" : " off");
  $("txtMon").textContent = d.monitor_on ? "ACTIVE" : "DISABLED";

  $("dotLock").className = "dot" + (d.locked ? " off" : " on");
  $("txtLock").textContent = d.locked ? "LOCKED" : "ONLINE";

  const body = $("cassettes"); body.innerHTML = "";
  d.cassettes.forEach((c, i) => {
    const init = initial[i] || c.count || 1;
    const pct = Math.max(0, Math.min(100, 100 * c.count / init));
    const cls = c.count === 0 ? "empty" : (pct < 30 ? "low" : "");
    const row = document.createElement("tr");
    row.innerHTML = `<td class="mono">${c.id}</td>
                      <td class="mono">$${c.denom}</td>
                      <td><div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div></td>
                      <td class="mono">${c.count}</td>`;
    body.appendChild(row);
  });

  $("dispensed").textContent = d.dispensed_total;
  $("remaining").textContent = d.remaining_notes;

  const f = $("flag");
  if (d.flag_released) {
    f.classList.add("show");
    f.textContent = "Vault empty — cashout proven. Flag released to operator.";
  } else {
    f.classList.remove("show");
  }
}

fetch("/status").then(r => r.json()).then(d => { d.cassettes.forEach((c, i) => initial[i] = c.count); });
setInterval(poll, 700);
poll();
