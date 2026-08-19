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
        <PageHeader
          title={destination.name}
          description="Destination details and tourism information."
        />

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
      </div>
    </main>
  );
}
