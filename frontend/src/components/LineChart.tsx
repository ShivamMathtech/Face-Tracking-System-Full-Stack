export function LineChart({series}:{series:number[]}){
 const w=640,h=180,p=18; const max=Math.max(1,...series), min=Math.min(0,...series); const pts=series.map((v,i)=>`${p+i*(w-2*p)/Math.max(1,series.length-1)},${h-p-(v-min)/(Math.max(1,max-min))*(h-2*p)}`).join(' ')
 return <svg className="line-chart" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopOpacity=".30"/><stop offset="1" stopOpacity="0"/></linearGradient></defs><polyline points={pts} fill="none" stroke="currentColor" strokeWidth="3"/><polyline points={`${p},${h-p} ${pts} ${w-p},${h-p}`} fill="url(#area)" stroke="none"/></svg>
}
