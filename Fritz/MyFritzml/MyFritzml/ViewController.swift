//
//  ViewController.swift
//  MyFritzml
//
//  Created by BossmediaNT on 18/12/18.
//  Copyright © 2018 Gtech Corporation. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    let model = HousePricer()
    
    @IBOutlet weak var crim: UITextField!
    
    @IBOutlet weak var zn: UITextField!
    
    @IBOutlet weak var price: UILabel!
    
    @IBOutlet weak var b: UITextField!
    
    @IBOutlet weak var ptratio: UITextField!
    
    @IBOutlet weak var medv: UITextField!
    
    @IBOutlet weak var lstat: UITextField!
    
    @IBOutlet weak var rad: UITextField!
    @IBOutlet weak var tax: UITextField!
    
    @IBOutlet weak var dis: UITextField!
    
    @IBOutlet weak var age: UITextField!
    
    @IBOutlet weak var rm: UITextField!
    
    @IBOutlet weak var nox: UITextField!
    
    @IBOutlet weak var chas: UITextField!
    
    @IBOutlet weak var indus: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        updated(rad);
    }
    
    @IBAction func updated(_ sender: Any) {
        guard let modeloutput = try? model.prediction(CRIM: Double(crim.text!)!, ZN: Double(zn.text!)!, INDUS: Double(indus.text!)!, CHAS: Double(chas.text!)!, NOX: Double(nox.text!)!, RM: Double(rm.text!)!, AGE: Double(age.text!)!, DIS: Double(dis.text!)!, RAD: Double(rad.text!)!, TAX: Double(tax.text!)!, PTRATIO: Double(ptratio.text!)!, B: Double(b.text!)!, LSTAT: Double(lstat.text!)!) else {
            fatalError("unexpected runtime error")
        }
        
        price.text = "$" + String(format: "%.2f",modeloutput.price);
    }


}

