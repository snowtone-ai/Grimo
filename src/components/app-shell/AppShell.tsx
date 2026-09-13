import Link from "next/link";import type { ReactNode } from "react";import { BottomNav } from "./BottomNav";
export function AppShell({title,children}:{title:string;children:ReactNode}){return <div className="app-shell"><header className="top-bar"><strong>{title}</strong><Link href="/settings" className="subtle-link">設定</Link></header><main className="screen">{children}</main><BottomNav/></div>}
