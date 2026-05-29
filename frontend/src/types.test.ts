import { describe, expect, it } from "vitest";

import { roleLabel } from "./types";

describe("roleLabel", () => {
  it("bilinen rol için okunabilir etiket döner", () => {
    expect(roleLabel("admin")).toBe("Admin");
    expect(roleLabel("content_creator")).toBe("Content Creator");
  });
});
