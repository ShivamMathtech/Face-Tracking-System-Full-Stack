import { useEffect, useRef, useState } from 'react'
import { Maximize2, Video } from 'lucide-react'
import { WS_BASE } from '../api'

export type Face={track_id:number;x:number;y:number;w:number;h:number;confidence:number;status:string}

export function CameraFeed({onFaces,onFps}:{onFaces:(f:Face[],size:{w:number,h:number})=>void;onFps:(n:number)=>void}){
 const [faces,setFaces]=useState<Face[]>([])
 const video=useRef<HTMLVideoElement>(null), canvas=useRef<HTMLCanvasElement>(null), ws=useRef<WebSocket|null>(null)
 useEffect(()=>{
   let timer:number|undefined
   navigator.mediaDevices?.getUserMedia({video:{width:{ideal:1280},height:{ideal:720}},audio:false}).then(stream=>{if(video.current){video.current.srcObject=stream; video.current.play()}}).catch(()=>{})
   const socket=new WebSocket(`${WS_BASE}/ws/track`); ws.current=socket
   socket.onmessage=e=>{const d=JSON.parse(e.data); if(d.type==='result'){setFaces(d.faces);onFaces(d.faces,d.width?{w:d.width,h:d.height}:{w:1280,h:720});onFps(d.fps)}}
   socket.onopen=()=>{timer=window.setInterval(()=>{const v=video.current,c=canvas.current;if(!v||!c||v.readyState<2||socket.readyState!==WebSocket.OPEN)return;c.width=640;c.height=Math.round(640*v.videoHeight/Math.max(1,v.videoWidth));const ctx=c.getContext('2d');ctx?.drawImage(v,0,0,c.width,c.height);socket.send(JSON.stringify({type:'frame',image:c.toDataURL('image/jpeg',.72)}))},120)}
   return ()=>{if(timer)clearInterval(timer);socket.close();const s=video.current?.srcObject as MediaStream|null;s?.getTracks().forEach(t=>t.stop())}
 },[])
 return <div className="camera-wrap"><div className="feed-header"><span><Video size={18}/> Live Camera Feed</span><div className="feed-actions"><span className="fps-pill">Live</span><Maximize2 size={18}/></div></div><div className="video-stage"><video ref={video} muted playsInline/><canvas ref={canvas} className="hidden-canvas"/>{faces.map(f=><div key={f.track_id} className="face-box" style={{left:`${f.x/640*100}%`,top:`${f.y/360*100}%`,width:`${f.w/640*100}%`,height:`${f.h/360*100}%`}}><span>Face-{String(f.track_id).padStart(2,"0")} <b>{(f.confidence*100).toFixed(1)}%</b></span></div>)}<div className="scanline"/></div><div className="feed-footer"><span>Faces: Live</span><span>Resolution: Browser Camera</span><span>Processing: CPU</span></div></div>
}
