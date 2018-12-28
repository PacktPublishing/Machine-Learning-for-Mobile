
/*
Created by Omid Alemi
Feb 17, 2017
 */

package com.example.vavinash.tensorflowsample;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Button;
import android.view.View;

import org.tensorflow.contrib.android.TensorFlowInferenceInterface;

public class MainActivity extends AppCompatActivity {

    private static final String MODEL_FILE = "file:///android_asset/ab2.pb";

    private static final int[] INPUT_SIZE = {1,3};

    private TensorFlowInferenceInterface inferenceInterface;

    static {
        System.loadLibrary("tensorflow_inference");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        inferenceInterface = new TensorFlowInferenceInterface();
        inferenceInterface.initializeTensorFlow(getAssets(), MODEL_FILE);


        final Button button = (Button) findViewById(R.id.button);

        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {

                final EditText editNum1 = (EditText) findViewById(R.id.editNum1);
                final EditText editNum2 = (EditText) findViewById(R.id.editNum2);


                float num1 = Float.parseFloat(editNum1.getText().toString());
                float num2 = Float.parseFloat(editNum2.getText().toString());


//                float[] inputFloats = {num1, num2, num3};
//
//                inferenceInterface.fillNodeFloat(INPUT_NODE, INPUT_SIZE, inputFloats);

                int[] i = {1};
                int[] a = {((int) num1)};
                int[] b = {((int) num2)};
                inferenceInterface.fillNodeInt("a",i,a);
                inferenceInterface.fillNodeInt("b",i,b);

                inferenceInterface.runInference(new String[] {"c"});

                int[] c = {0};
                inferenceInterface.readNodeInt("c", c);

                final TextView textViewR = (TextView) findViewById(R.id.txtViewResult);
                textViewR.setText(Integer.toString(c[0]));
            }
        });

    }

}