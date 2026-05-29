import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import PlaceholderPage from "./PlaceholderPage";

describe("PlaceholderPage", () => {
  it("verilen başlığı gösterir", () => {
    render(<PlaceholderPage title="Test Başlık" />);
    expect(screen.getByText("Test Başlık")).toBeInTheDocument();
  });
});
