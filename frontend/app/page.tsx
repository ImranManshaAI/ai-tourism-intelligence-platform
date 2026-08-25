import Link from "next/link";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { mockDestinations } from "../mocks/destinations";

const navigationItems = [
  { label: "Dashboard", href: "/" },
  { label: "Destinations", href: "/destinations" },
  { label: "Documents", href: "/documents" },
  { label: "AI Assistant", href: "/ai-assistant" },
];

export default function Home() {
  const summaryItems = [
    {
      label: "Destinations",
      value: String(mockDestinations.length),
      description: "Available tourism destinations",
    },
    {
      label: "Documents",
      value: "0",
      description: "Knowledge documents",
    },
    {
      label: "AI Assistant",
      value: "Ready",
      description: "Intelligence services",
    },
  ];

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

          <nav className="flex-1 px-3 py-5" aria-label="Main navigation">
            <div className="space-y-1">
              {navigationItems.map((item, index) => (
                <Link
                  key={item.label}
                  href={item.href}
                  className={`block rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                    index === 0
                      ? "bg-white/15 text-white"
                      : "text-white/75 hover:bg-white/10 hover:text-white"
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </nav>

          <div className="border-t border-white/10 px-6 py-4">
            <p className="text-xs text-white/50">Administration Platform</p>
            <p className="mt-1 text-sm text-white/80">Phase 1</p>
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

          <div className="mx-auto w-full max-w-7xl p-5 md:p-8">
            <PageHeader
              title="Dashboard"
              description="Manage tourism intelligence, destinations, documents, and AI-powered services."
            />

            <section
              className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
              aria-label="Platform summary"
            >
              {summaryItems.map((item) => (
                <Card key={item.label} className="p-5">
                  <p className="text-sm font-medium text-text-secondary">
                    {item.label}
                  </p>

                  <p className="mt-2 text-2xl font-semibold text-text-primary">
                    {item.value}
                  </p>

                  <p className="mt-1 text-sm text-text-muted">
                    {item.description}
                  </p>
                </Card>
              ))}
            </section>

            <section className="mt-6">
              <h2 className="text-lg font-semibold text-text-primary">
                Quick Actions
              </h2>

              <div className="mt-4 grid gap-4 md:grid-cols-3">
                <Link
                  href="/destinations"
                  className="block rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <Card className="h-full p-5 transition-shadow hover:shadow-md">
                    <h3 className="text-base font-semibold text-text-primary">
                      Manage Destinations
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-text-secondary">
                      Explore available tourism destinations and view their
                      details.
                    </p>
                  </Card>
                </Link>

                <Link
                  href="/documents"
                  className="block rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <Card className="h-full p-5 transition-shadow hover:shadow-md">
                    <h3 className="text-base font-semibold text-text-primary">
                      Manage Documents
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-text-secondary">
                      View and manage knowledge documents for the platform.
                    </p>
                  </Card>
                </Link>

                <Link
                  href="/ai-assistant"
                  className="block rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                >
                  <Card className="h-full p-5 transition-shadow hover:shadow-md">
                    <h3 className="text-base font-semibold text-text-primary">
                      Open AI Assistant
                    </h3>

                    <p className="mt-2 text-sm leading-6 text-text-secondary">
                      Ask questions about tourism information and platform
                      knowledge.
                    </p>
                  </Card>
                </Link>
              </div>
            </section>

            <section className="mt-6">
              <Card className="p-6">
                <h2 className="text-lg font-semibold text-text-primary">
                  Welcome to ATIP
                </h2>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-text-secondary">
                  The application shell is now connected to the frontend
                  foundation. Destination management, document intelligence,
                  authentication, and AI assistant features will be added
                  incrementally.
                </p>
              </Card>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}