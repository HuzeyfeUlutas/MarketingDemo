import { describe, expect, it } from "vitest";

import { clientStatusLabel, contentStatusLabel, platformLabel, roleLabel } from "./types";

describe("roleLabel", () => {
  it("bilinen rol için okunabilir etiket döner", () => {
    expect(roleLabel("admin")).toBe("Admin");
    expect(roleLabel("content_creator")).toBe("Content Creator");
  });
});

describe("client/platform etiketleri", () => {
  it("müşteri durumu etiketleri", () => {
    expect(clientStatusLabel("active")).toBe("Aktif");
    expect(clientStatusLabel("archived")).toBe("Arşivlendi");
  });

  it("platform etiketleri", () => {
    expect(platformLabel("x")).toBe("X (Twitter)");
    expect(platformLabel("instagram")).toBe("Instagram");
  });

  it("içerik durumu etiketleri", () => {
    expect(contentStatusLabel("pending_review")).toBe("İncelemede");
    expect(contentStatusLabel("published")).toBe("Yayınlandı");
  });
});
