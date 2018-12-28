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


    let model = cancermodel()
    
    @IBOutlet weak var meanradius: UITextField!
    @IBOutlet weak var cancertype: UILabel!
    
    @IBOutlet weak var meanperimeter: UITextField!
    
    @IBOutlet weak var meanarea: UITextField!
    
    @IBOutlet weak var meanconcavity: UITextField!
    
    @IBOutlet weak var meanconcavepoints: UITextField!
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func viewDidLoad() {
        super.viewDidLoad();
        updated(meanconcavepoints);
    }
    
    
    @IBAction func updated(_ sender: Any) {
        guard let modeloutput = try? model.prediction(mean_radius: Double(meanradius.text!)!, mean_perimeter: Double(meanperimeter.text!)!, mean_area: Double(meanarea.text!)!, mean_concavity: Double(meanconcavity.text!)!, mean_concave_points: Double(meanconcavepoints.text!)!) else {
            fatalError("unexpected runtime error")
        }
        
        cancertype.text = modeloutput.typeofcancer;
    }

    
    
}

