import Link from "next/link";
import { AppShell } from "../components/layout/AppShell";
import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { mockDestinations } from "../mocks/destinations";

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
    <AppShell activePath="/">
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
    </AppShell>
  );
}