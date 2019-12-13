package com.example.gesturerecognition;

import android.content.Intent;
import android.content.res.AssetFileDescriptor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.concurrent.TimeUnit;

import okhttp3.MultipartBody.Part;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import org.apache.commons.io.IOUtils;

public class Screen3 extends AppCompatActivity {
    private static final int VIDEO_CAPTURE = 101;
    byte[] mediaFile;
    String GESTURE_ID;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.screen3);
        GESTURE_ID = getIntent().getStringExtra("GESTURE_ID");
        final Button uploadBtn=findViewById(R.id.uploadButton);
        uploadBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                upload("/upload");
            }
        });
        final Button tos1Btn=findViewById(R.id.tos1Button);
        tos1Btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                to_s1();
            }
        });
        final Button classifyBtn=findViewById(R.id.classifyButton);
        classifyBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                upload("/classify");
            }
        });
        startRecording();
    }

    private void startRecording() {
        Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        intent.putExtra(MediaStore.EXTRA_DURATION_LIMIT,5);
        startActivityForResult(intent, VIDEO_CAPTURE);
    }

    protected void onActivityResult(int requestCode,
                                    int resultCode, Intent data) {

        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == VIDEO_CAPTURE) {
            if (resultCode == RESULT_OK) {
                Uri uri = data.getData();
                try {
                    InputStream is = getContentResolver().openInputStream(uri);
                    mediaFile = IOUtils.toByteArray(is);
                } catch (Exception e) {
                    System.out.println(e);
                }


                Toast.makeText(this, "Video has been saved ", Toast.LENGTH_LONG).show();
            } else if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, "Video recording cancelled.",
                        Toast.LENGTH_LONG).show();
            } else {
                Toast.makeText(this, "Failed to record video",
                        Toast.LENGTH_LONG).show();
            }
        }
    }

    void upload(String extension)
    {

        EditText ip = findViewById(R.id.IPAddress);
        EditText port = findViewById(R.id.Port);
        String url = "http://" + ip.getText().toString() + ":" + port.getText().toString() + extension;
        //System.out.println("URL : "+url);
        EditText name = findViewById(R.id.name);
        EditText num = findViewById(R.id.num);


        OkHttpClient client = new OkHttpClient.Builder()
                .connectTimeout(300, TimeUnit.SECONDS)
                .writeTimeout(300, TimeUnit.SECONDS)
                .readTimeout(300, TimeUnit.SECONDS)
                .build();


        MultipartBody requestBody = new MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart(name.getText().toString(),   GESTURE_ID + "_" + num.getText().toString() + "_" + name.getText().toString() + ".mp4", RequestBody.create(MediaType.parse("video/mp4"), mediaFile))
                .build();

        Request request = new Request.Builder()
                .url(url)
                .post(requestBody)
                .build();


        client.newCall(request).enqueue(new Callback() {

            @Override
            public void onFailure(Call call, IOException e) {
                TextView result = findViewById(R.id.Result);
                result.setText(e.toString());
            }

            @Override
            public void onResponse(Call call, Response response) {
                TextView result = findViewById(R.id.Result);
                try {
                    result.setText(response.body().string());
                } catch(IOException e) {
                    result.setText(e.toString());
                }
            }
        });

    }

    void to_s1() {
        // Navigate to Screen3
        Intent intent = new Intent(this, Screen1.class);
        startActivity(intent);
    }

}
