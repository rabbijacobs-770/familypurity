import Foundation
import PDFKit
import AppKit
// Dump text runs as JSON lines: page, font name, size, baseline offset, text
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
var out: [[String: Any]] = []
for i in 0..<doc.pageCount {
  guard let page = doc.page(at: i), let s = page.attributedString else { continue }
  s.enumerateAttributes(in: NSRange(location: 0, length: s.length)) { attrs, range, _ in
    let t = (s.string as NSString).substring(with: range)
    let f = attrs[.font] as? NSFont
    let bo = (attrs[.baselineOffset] as? NSNumber)?.doubleValue ?? 0
    out.append(["p": i+1, "f": f?.fontName ?? "?", "s": Double(f?.pointSize ?? 0), "b": bo, "t": t])
  }
}
let data = try JSONSerialization.data(withJSONObject: out)
try data.write(to: URL(fileURLWithPath: a[2]))
print(a[1].split(separator: "/").last!, out.count, "runs")
