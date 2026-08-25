"use client";

import { useState } from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { PageHeader } from "../../components/ui/PageHeader";
import { Textarea } from "../../components/ui/Textarea";

const exampleQuestions = [
  "What are the best tourist destinations in Bahawalpur?",
  "What facilities are available at this destination?",
  "What should tourists know before visiting?",
];

export default function AiAssistantPage() {
  const [question, setQuestion] = useState("");
  const [submittedQuestion, setSubmittedQuestion] = useState("");

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    setSubmittedQuestion(trimmedQuestion);
    setQuestion("");
  }

  function handleExampleQuestion(exampleQuestion: string) {
    setQuestion(exampleQuestion);
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="mx-auto w-full max-w-5xl p-5 md:p-8">
        <PageHeader
          title="AI Assistant"
          description="Ask questions about tourism information and platform knowledge."
        />

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <Card className="p-6 lg:col-span-2">
            <h2 className="text-lg font-semibold text-text-primary">
              Ask the tourism assistant
            </h2>

            <p className="mt-2 text-sm leading-6 text-text-secondary">
              The AI service is not connected yet. You can test the question
              interface before connecting it to the backend API.
            </p>

            <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
              <Textarea
                aria-label="Tourism question"
                placeholder="Ask a question about destinations, travel, or tourism information..."
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
              />

              <div className="flex justify-end">
                <Button type="submit" disabled={!question.trim()}>
                  Ask Assistant
                </Button>
              </div>
            </form>

            {submittedQuestion && (
              <div className="mt-6 rounded-lg border border-border bg-surface-muted p-4">
                <div className="flex items-start justify-between gap-4">
                  <p className="text-sm font-medium text-text-primary">
                    Your question
                  </p>

                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => setSubmittedQuestion("")}
                  >
                    Clear
                  </Button>
                </div>

                <p className="mt-2 text-sm leading-6 text-text-secondary">
                  {submittedQuestion}
                </p>

                <div className="mt-4 border-t border-border pt-4">
                  <p className="text-sm font-medium text-text-primary">
                    Assistant response
                  </p>

                  <p className="mt-2 text-sm leading-6 text-text-muted">
                    The backend AI response will appear here after the API is
                    connected.
                  </p>
                </div>
              </div>
            )}
          </Card>

          <Card className="p-6">
            <h2 className="text-base font-semibold text-text-primary">
              Example questions
            </h2>

            <p className="mt-2 text-sm leading-6 text-text-secondary">
              Select an example to quickly test the assistant interface.
            </p>

            <div className="mt-4 space-y-3">
              {exampleQuestions.map((exampleQuestion) => (
                <button
                  key={exampleQuestion}
                  type="button"
                  onClick={() => handleExampleQuestion(exampleQuestion)}
                  className="w-full rounded-lg border border-border bg-surface-muted px-4 py-3 text-left text-sm leading-6 text-text-secondary transition-colors hover:bg-surface focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                >
                  {exampleQuestion}
                </button>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </main>
  );
}