//
//  ViewController.swift
//  ImageRecognitionCoreML
//
//  Created by Mohammad Azam on 9/4/17.
//  Copyright © 2017 Mohammad Azam. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var pictureImageView :UIImageView!
    @IBOutlet weak var titleLabel :UILabel!
    
    private var model : converted = converted()
    
    var content : [ String : String ] = [
        "cheeseburger" : "A cheeseburger is a hamburger topped with cheese. Traditionally, the slice of cheese is placed on top of the meat patty, but the burger can include many variations in structure, ingredients, and composition.\nIt has 303 calories per 100 grams.",
        "carbonara" : "Carbonara is an Italian pasta dish from Rome made with egg, hard cheese, guanciale, and pepper. The recipe is not fixed by a specific type of hard cheese or pasta. The cheese is usually Pecorino Romano.",
        "meat loaf" : "Meatloaf is a dish of ground meat mixed with other ingredients and formed into a loaf shape, then baked or smoked. The shape is created by either cooking it in a loaf pan, or forming it by hand on a flat pan.\nIt has 149 calories / 100 grams",
        "pizza" : "Pizza is a traditional Italian dish consisting of a yeasted flatbread typically topped with tomato sauce and cheese and baked in an oven. It can also be topped with additional vegetables, meats, and condiments, and can be made without cheese.\nIt has 285 calories / 100 grams"
                                    ]
    
    
    
    let images = ["burger.jpg","meatloaf.png","pasta.jpg", "pizza.png"]
    var index = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        nextImage()
    }
    
    @IBAction func nextButtonPressed() {
        nextImage()
    }

    func nextImage() {
        defer { index = index < images.count - 1 ? index + 1 : 0 }

        let filename = images[index]
        guard let img = UIImage(named: filename) else {
            self.titleLabel.text = "Failed to load image \(filename)"
            return
        }

        self.pictureImageView.image = img

        let resizedImage = img.resizeTo(size: CGSize(width: 224, height: 224))

        guard let buffer = resizedImage.toBuffer() else {
            self.titleLabel.text = "Failed to make buffer from image \(filename)"
            return
        }

        do {
            
            let prediction = try self.model.prediction(input: convertedInput(input__0: buffer))
            if content.keys.contains(prediction.classLabel) {
                self.titleLabel.text = content[prediction.classLabel]
            }
            else
            {
                self.titleLabel.text = prediction.classLabel;
            }
            
        } catch let error {
            self.titleLabel.text = error.localizedDescription
        }

    }

}

