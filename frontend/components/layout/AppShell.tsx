import Link from "next/link";
import { ReactNode } from "react";

type AppShellProps = {
  children: ReactNode;
  activePath: "/" | "/destinations" | "/documents" | "/ai-assistant";
};

const navigationItems = [
  { label: "Dashboard", href: "/" },
  { label: "Destinations", href: "/destinations" },
  { label: "Documents", href: "/documents" },
  { label: "AI Assistant", href: "/ai-assistant" },
] as const;

export function AppShell({
  children,
  activePath,
}: AppShellProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex min-h-screen">
        <aside className="hidden w-64 shrink-0 border-r border-border bg-primary text-white md:flex md:flex-col">
          <div className="border-b border-white/10 px-6 py-5">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-white/60">
              ATIP
            </p>

            <h2 className="mt-1 text-lg font-semibold">
              Tourism Intelligence
            </h2>
          </div>

          <nav
            className="flex-1 px-3 py-5"
            aria-label="Main navigation"
          >
            <div className="space-y-1">
              {navigationItems.map((item) => {
                const isActive = item.href === activePath;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`block rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-white/15 text-white"
                        : "text-white/75 hover:bg-white/10 hover:text-white"
                    }`}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </nav>

          <div className="border-t border-white/10 px-6 py-4">
            <p className="text-xs text-white/50">
              Administration Platform
            </p>

            <p className="mt-1 text-sm text-white/80">
              Phase 1
            </p>
          </div>
        </aside>

        <main className="min-w-0 flex-1">
          <div className="border-b border-border bg-surface px-5 py-4 md:hidden">
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-text-muted">
              ATIP
            </p>

            <p className="mt-1 font-semibold text-text-primary">
              Tourism Intelligence
            </p>
          </div>

          {children}
        </main>
      </div>
    </div>
  );
}