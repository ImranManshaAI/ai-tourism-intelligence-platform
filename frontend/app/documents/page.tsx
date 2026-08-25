import { AppShell } from "../../components/layout/AppShell";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { PageHeader } from "../../components/ui/PageHeader";

const supportedDocumentTypes = [
  "Tourism guides",
  "Destination information",
  "Travel policies",
  "Research documents",
];

export default function DocumentsPage() {
  return (
    <AppShell activePath="/documents">
      <div className="mx-auto w-full max-w-7xl p-5 md:p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <PageHeader
            title="Documents"
            description="Manage knowledge documents used by the tourism intelligence platform."
          />

          <Button disabled>Upload Document</Button>
        </div>

        <div className="mt-6">
          <EmptyState
            title="No documents available"
            description="Document upload and knowledge management will be connected in a future implementation step."
          />
        </div>

        <section className="mt-6" aria-labelledby="supported-document-types">
          <Card className="p-5">
            <h2
              id="supported-document-types"
              className="text-lg font-semibold text-text-primary"
            >
              Supported document types
            </h2>

            <p className="mt-2 text-sm leading-6 text-text-secondary">
              The document knowledge base will support tourism-related
              information for future search and AI assistant features.
            </p>

            <ul className="mt-4 grid gap-3 sm:grid-cols-2">
              {supportedDocumentTypes.map((documentType) => (
                <li
                  key={documentType}
                  className="rounded-lg border border-border bg-surface-muted px-4 py-3 text-sm text-text-secondary"
                >
                  {documentType}
                </li>
              ))}
            </ul>
          </Card>
        </section>
      </div>
    </AppShell>
  );
}