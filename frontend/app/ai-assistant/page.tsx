import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { PageHeader } from "../../components/ui/PageHeader";
import { Textarea } from "../../components/ui/Textarea";

export default function AiAssistantPage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto w-full max-w-5xl p-5 md:p-8">
        <PageHeader
          title="AI Assistant"
          description="Ask questions about tourism information and platform knowledge."
        />

        <Card className="mt-6 p-6">
          <h2 className="text-lg font-semibold text-text-primary">
            Ask the tourism assistant
          </h2>

          <p className="mt-2 text-sm leading-6 text-text-secondary">
            The AI service is not connected yet. This interface will be linked
            to a secure backend API in a later implementation step.
          </p>

          <form className="mt-6 space-y-4">
            <Textarea
              aria-label="Tourism question"
              placeholder="Ask a question about destinations, travel, or tourism information..."
              disabled
            />

            <div className="flex justify-end">
              <Button type="submit" disabled>
                Ask Assistant
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </main>
  );
}
