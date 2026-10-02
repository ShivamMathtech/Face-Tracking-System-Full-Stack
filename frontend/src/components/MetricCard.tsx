import { LucideIcon } from 'lucide-react'
export function MetricCard({icon:Icon,label,value,tone='blue'}:{icon:LucideIcon,label:string,value:string|number,tone?:string}){
 return <div className="metric-card"><div className={`metric-icon ${tone}`}><Icon size={20}/></div><div><div className="metric-label">{label}</div><div className="metric-value">{value}</div></div></div>
}
