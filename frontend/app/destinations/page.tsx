import Link from "next/link";
import { AppShell } from "../../components/layout/AppShell";
import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { PageHeader } from "../../components/ui/PageHeader";
import { mockDestinations } from "../../mocks/destinations";

export default function DestinationsPage() {
  return (
    <AppShell activePath="/destinations">
      <div className="mx-auto w-full max-w-7xl p-5 md:p-8">
        <PageHeader
          title="Destinations"
          description="Manage and explore tourism destinations available in the platform."
        />

        {mockDestinations.length === 0 ? (
          <div className="mt-6">
            <EmptyState
              title="No destinations found"
              description="There are currently no destinations available."
            />
          </div>
        ) : (
          <section
            className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3"
            aria-label="Tourism destinations"
          >
            {mockDestinations.map((destination) => (
              <Link
                key={destination.id}
                href={`/destinations/${destination.id}`}
                className="block rounded-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <Card className="h-full p-5 transition-shadow hover:shadow-md">
                  <h2 className="text-lg font-semibold text-text-primary">
                    {destination.name}
                  </h2>

                  <p className="mt-2 text-sm leading-6 text-text-secondary">
                    {destination.description}
                  </p>

                  <p className="mt-4 text-sm font-medium text-accent">
                    View details →
                  </p>
                </Card>
              </Link>
            ))}
          </section>
        )}
      </div>
    </AppShell>
  );
}
