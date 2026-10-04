import Foundation
import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let page = doc.page(at: Int(a[2])! - 1)!
let img = page.thumbnail(of: NSSize(width: Double(a[4])!, height: Double(a[4])! * 1.3), for: .mediaBox)
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[3]))
