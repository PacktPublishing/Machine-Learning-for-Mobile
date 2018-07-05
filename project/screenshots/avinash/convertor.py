import tfcoreml as tf_converter
tf_converter.convert(tf_model_path = 'retrained_graph.pb',
                     mlmodel_path = 'converted.mlmodel',
                     output_feature_names = ['final_result:0'],
                     image_input_names = 'input:0',
                     class_labels = 'retrained_labels.txt',
                     red_bias = -1,
                     green_bias = -1,
                     blue_bias = -1,
                     image_scale = 2.0/224.0
                     )
