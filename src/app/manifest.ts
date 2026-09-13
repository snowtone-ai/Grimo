import type { MetadataRoute } from "next";
export default function manifest():MetadataRoute.Manifest{return{name:"Grimo",short_name:"Grimo",description:"グリモと触れ合うためのタスク管理PWA",start_url:"/",display:"standalone",background_color:"#f6f5ef",theme_color:"#f6f5ef",orientation:"portrait"};}
