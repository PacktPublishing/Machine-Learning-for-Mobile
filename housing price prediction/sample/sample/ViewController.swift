//
//  ViewController.swift
//  sample
//
//  Created by BossmediaNT on 24/01/18.
//  Copyright © 2018 BossmediaNT. All rights reserved.
//

import UIKit
import CoreML



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
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewDidLoad() {
        super.viewDidLoad();
        updated(rad);
    }
    
    
    @IBAction func updated(_ sender: Any) {
        guard let modeloutput = try? model.prediction(CRIM: Double(crim.text!)!, ZN: Double(zn.text!)!, INDUS: Double(indus.text!)!, CHAS: Double(chas.text!)!, NOX: Double(nox.text!)!, RM: Double(rm.text!)!, AGE: Double(age.text!)!, DIS: Double(dis.text!)!, RAD: Double(rad.text!)!, TAX: Double(tax.text!)!, PTRATIO: Double(ptratio.text!)!, B: Double(b.text!)!, LSTAT: Double(lstat.text!)!) else {
            fatalError("unexpected runtime error")
        }
        
        price.text = "$" + String(format: "%.2f",modeloutput.price);
    }

    
    
}

