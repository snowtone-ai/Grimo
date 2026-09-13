"use client";
import { useEffect } from "react";import { useRouter } from "next/navigation";import { readStartPage } from "@/domain/preferences/start-page";
export default function LaunchPage(){const router=useRouter();useEffect(()=>{router.replace(readStartPage()==="grimo"?"/grimo":"/tasks");},[router]);return <main className="launch"><div className="launch-mark">Grimo</div><p>起動しています…</p></main>}
