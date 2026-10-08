import React, {useEffect, useState} from 'react'
import {createRoot} from 'react-dom/client'
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer} from 'recharts'
import './styles.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Stat({label,value,sub}){return <div className="stat"><div className="muted">{label}</div><div className="big">{value}</div><div className="muted">{sub}</div></div>}

function App(){
  const [data,setData]=useState(null)
  const [sku,setSku]=useState('')
  const [forecast,setForecast]=useState([])
  const [loading,setLoading]=useState(true)
  const [msg,setMsg]=useState('')

  const load=async()=>{setLoading(true); const r=await fetch(`${API}/api/dashboard`); const j=await r.json(); setData(j); if(!sku && j.inventory[0]) setSku(j.inventory[0].sku); setLoading(false)}
  useEffect(()=>{load()},[])
  useEffect(()=>{if(sku) fetch(`${API}/api/forecast/${sku}?horizon=14`).then(r=>r.json()).then(j=>setForecast(j.forecast))},[sku])

  const retrain=async()=>{setMsg('Refreshing models...'); await fetch(`${API}/api/retrain`,{method:'POST'}); setMsg('Models refreshed'); load()}
  if(loading || !data) return <div className="center">Loading SupplySense AI…</div>

  return <div>
    <header>
      <div><div className="brand">SupplySense <span>AI</span></div><div className="tag">Demand intelligence for smarter inventory</div></div>
      <button onClick={retrain}>↻ Refresh Models</button>
    </header>
    <main>
      {msg && <div className="toast">{msg}</div>}
      <section className="stats">
        <Stat label="TOTAL SKUs" value={data.summary.total_skus} sub="Tracked products"/>
        <Stat label="STOCKOUT RISK" value={data.summary.stockout_risk} sub="Immediate attention"/>
        <Stat label="OVERSTOCK RISK" value={data.summary.overstock_risk} sub="Capital at risk"/>
        <Stat label="INVENTORY VALUE" value={`$${data.summary.inventory_value.toLocaleString()}`} sub="Current stock value"/>
      </section>

      <section className="grid">
        <div className="panel">
          <div className="panelhead"><div><h2>Demand Forecast</h2><p>14-day AI prediction</p></div>
            <select value={sku} onChange={e=>setSku(e.target.value)}>{data.inventory.map(x=><option key={x.sku}>{x.sku}</option>)}</select>
          </div>
          <ResponsiveContainer width="100%" height={310}>
            <LineChart data={forecast}><CartesianGrid strokeDasharray="3 3" opacity=".15"/><XAxis dataKey="date"/><YAxis/><Tooltip/><Line type="monotone" dataKey="predicted_demand" strokeWidth={3} dot={false}/></LineChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>Inventory Alerts</h2><p>Prioritized by forecasted risk</p>
          {data.alerts.length===0 ? <div className="empty">All inventory levels look healthy.</div> :
          data.alerts.map(a=><div className="alert" key={a.sku}><div className={`dot ${a.severity}`}></div><div className="alertbody"><b>{a.sku} · {a.name}</b><span className="pill">{a.risk}</span><p>{a.message}</p><small>Recommended order: <b>{a.recommended_order} units</b></small></div></div>)}
        </div>
      </section>

      <section className="panel">
        <div className="panelhead"><div><h2>Inventory Health</h2><p>Stock position against forecast</p></div></div>
        <div className="tablewrap"><table><thead><tr><th>SKU</th><th>PRODUCT</th><th>STOCK</th><th>AVG DAILY DEMAND</th><th>LEAD-TIME PROJECTION</th><th>STATUS</th><th>ORDER</th></tr></thead>
        <tbody>{data.inventory.map(x=><tr key={x.sku}><td><b>{x.sku}</b></td><td>{x.name}</td><td>{x.current_stock}</td><td>{x.avg_daily_demand}</td><td>{x.projected_after_lead_time}</td><td><span className={`status ${x.severity}`}>{x.risk}</span></td><td>{x.recommended_order}</td></tr>)}</tbody></table></div>
      </section>
    </main>
    <footer>SupplySense AI · ML-powered inventory intelligence · Demo data included</footer>
  </div>
}
createRoot(document.getElementById('root')).render(<App/>)
