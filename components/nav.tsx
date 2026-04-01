import type { Route } from "next";
import Link from "next/link";

type NavProps = {
  current: string;
};

export function AppNav({ current }: NavProps) {
  const links = [
    { href: "/admin/sellers" as Route, label: "Admin Sellers" },
    { href: "/admin/events" as Route, label: "Admin Evenements" }
  ];

  return (
    <nav className="nav">
      <div>
        <span className="eyebrow">MOMENT x vivenu</span>
      </div>
      <div className="nav-links">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`nav-link ${current === link.href ? "active" : ""}`}
          >
            {link.label}
          </Link>
        ))}
      </div>
    </nav>
  );
}
