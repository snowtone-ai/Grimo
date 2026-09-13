"use client";
import Link from "next/link";import { usePathname } from "next/navigation";
const items=[{href:"/tasks",label:"タスク"},{href:"/grimo",label:"グリモ"},{href:"/calendar",label:"カレンダー"}] as const;
export function BottomNav(){const pathname=usePathname();return <nav className="bottom-nav" aria-label="メイン"><div className="bottom-nav__inner">{items.map(item=><Link key={item.href} href={item.href} aria-current={pathname.startsWith(item.href)?"page":undefined} className={pathname.startsWith(item.href)?"nav-item is-active":"nav-item"}><span className="nav-dot" aria-hidden="true"/><span>{item.label}</span></Link>)}</div></nav>}
