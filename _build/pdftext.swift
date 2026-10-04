import Foundation
import PDFKit
let args = CommandLine.arguments
guard args.count >= 3, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { print("open failed"); exit(1) }
var out = ""
for i in 0..<doc.pageCount { if let p = doc.page(at: i) { out += "\n=== PAGE \(i+1) ===\n" + (p.string ?? "") } }
try out.write(toFile: args[2], atomically: true, encoding: .utf8)
print("\(args[1].split(separator: "/").last!): \(doc.pageCount) pages, \(out.count) chars")
