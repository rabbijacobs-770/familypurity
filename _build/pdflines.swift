import Foundation
import PDFKit
import AppKit
// Dump every visual line with its position and styled runs, so text can be read top-to-bottom.
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
var out: [[String: Any]] = []
for i in 0..<doc.pageCount {
  guard let page = doc.page(at: i), let sel = page.selection(for: page.bounds(for: .mediaBox)) else { continue }
  for line in sel.selectionsByLine() {
    let b = line.bounds(for: page)
    guard let s = line.attributedString, s.length > 0 else { continue }
    var runs: [[String: Any]] = []
    s.enumerateAttributes(in: NSRange(location: 0, length: s.length)) { attrs, range, _ in
      let t = (s.string as NSString).substring(with: range)
      let f = attrs[.font] as? NSFont
      runs.append(["f": f?.fontName ?? "?", "s": Double(f?.pointSize ?? 0), "t": t])
    }
    out.append(["p": i+1, "x": Double(b.minX), "w": Double(b.width), "y": Double(b.maxY), "h": Double(b.height), "runs": runs])
  }
}
try JSONSerialization.data(withJSONObject: out).write(to: URL(fileURLWithPath: a[2]))
print(a[1].split(separator: "/").last!, out.count, "lines")
