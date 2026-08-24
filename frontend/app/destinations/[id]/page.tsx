import Link from "next/link";
import { notFound } from "next/navigation";
import { Badge } from "../../../components/ui/Badge";
import { Card } from "../../../components/ui/Card";
import { PageHeader } from "../../../components/ui/PageHeader";
import { mockDestinations } from "../../../mocks/destinations";

type DestinationPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function DestinationPage({
  params,
}: DestinationPageProps) {
  const { id } = await params;

  const destination = mockDestinations.find((item) => item.id === id);

  if (!destination) {
    notFound();
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto w-full max-w-5xl p-5 md:p-8">
        <Link
          href="/destinations"
          className="inline-flex text-sm font-medium text-accent hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          ← Back to Destinations
        </Link>

        <div className="mt-4">
          <PageHeader
            title={destination.name}
            description="Destination details and tourism information."
          />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <Card className="p-6 lg:col-span-2">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="success">Available</Badge>
            </div>

            <h2 className="mt-4 text-lg font-semibold text-text-primary">
              About this destination
            </h2>

            <p className="mt-2 text-sm leading-7 text-text-secondary">
              {destination.description}
            </p>
          </Card>

          <Card className="p-6">
            <h2 className="text-base font-semibold text-text-primary">
              Information
            </h2>

            <dl className="mt-4 space-y-4">
              <div>
                <dt className="text-xs font-medium uppercase tracking-wide text-text-muted">
                  Opening hours
                </dt>
                <dd className="mt-1 text-sm text-text-secondary">
                  {destination.opening_hours ?? "Verify before visit"}
                </dd>
              </div>

              <div>
                <dt className="text-xs font-medium uppercase tracking-wide text-text-muted">
                  Ticket price
                </dt>
                <dd className="mt-1 text-sm text-text-secondary">
                  {destination.ticket_price ?? "Verify before visit"}
                </dd>
              </div>

              <div>
                <dt className="text-xs font-medium uppercase tracking-wide text-text-muted">
                  Location
                </dt>
                <dd className="mt-1 text-sm text-text-secondary">
                  {destination.latitude !== null &&
                  destination.longitude !== null
                    ? `${destination.latitude}, ${destination.longitude}`
                    : "Location coordinates unavailable"}
                </dd>
              </div>
            </dl>
          </Card>
        </div>

        {destination.facilities.length > 0 ? (
          <section className="mt-6">
            <Card className="p-6">
              <h2 className="text-lg font-semibold text-text-primary">
                Facilities
              </h2>

              <ul className="mt-4 grid gap-2 sm:grid-cols-2">
                {destination.facilities.map((facility) => (
                  <li
                    key={facility}
                    className="rounded-lg bg-surface-muted px-3 py-2 text-sm text-text-secondary"
                  >
                    {facility}
                  </li>
                ))}
              </ul>
            </Card>
          </section>
        ) : null}

        {destination.travel_tips.length > 0 ? (
          <section className="mt-6">
            <Card className="p-6">
              <h2 className="text-lg font-semibold text-text-primary">
                Travel Tips
              </h2>

              <ul className="mt-4 space-y-2">
                {destination.travel_tips.map((tip) => (
                  <li
                    key={tip}
                    className="text-sm leading-6 text-text-secondary"
                  >
                    {tip}
                  </li>
                ))}
              </ul>
            </Card>
          </section>
        ) : null}
      </div>
    </main>
  );
}