package com.example.gesturerecognition;

import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;

import java.net.FileNameMap;


public class Screen2 extends AppCompatActivity implements View.OnClickListener {
    String GESTURE_ID;

    private void startDownload(final String GESTURE_ID, final String DOWNLOAD_URL) {
        new DownloadFileAsync().execute(GESTURE_ID, DOWNLOAD_URL);
    }

    class DownloadFileAsync extends AsyncTask<String, String, String> {
        String gestureID = "";
        @Override
        protected String doInBackground(String... params) {
            // params[0] => gestureID
            // params[1] => videoURL
            gestureID = params[0];
            try {
                // Create request for android download manager
                DownloadManager downloadManager = (DownloadManager) getSystemService(Context.DOWNLOAD_SERVICE);
                DownloadManager.Request request = new DownloadManager.Request(Uri.parse(params[1]));
                request.setAllowedNetworkTypes(DownloadManager.Request.NETWORK_WIFI |
                        DownloadManager.Request.NETWORK_MOBILE);

                // set title and description
                request.setTitle("Data Download");
                request.setDescription("Android Data download using DownloadManager.");

                request.allowScanningByMediaScanner();
                request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                //set the local destination for download file to a path within the application's external files directory
                request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, params[0] + "_gesture.mp4");
                request.setMimeType("*/*");
                // Check that the SDCard is mounted
                if (downloadManager != null && isExternalStorageWritable())
                    downloadManager.enqueue(request);
                else
                    Toast.makeText(getApplicationContext(), "Don't have permission to write to external storage. ", Toast.LENGTH_LONG).show();
            } catch (Exception e) {
                Log.d("Error....", e.toString());
            }

            return null;
        }

        @Override
        protected void onPostExecute(String s) {
            Toast.makeText(getApplicationContext(), "Video Download complete. ", Toast.LENGTH_SHORT).show();
            try {
                Thread.sleep(2000);
            } catch (InterruptedException ie) {
                Toast.makeText(getApplicationContext(), ie.getMessage(), Toast.LENGTH_SHORT).show();
            } finally {
                showVideo(gestureID);
                final Button replayBtn=findViewById(R.id.replayBtn);
                replayBtn.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        showVideo(gestureID);
                    }
                });


            }
        }
    }

    /* Checks if external storage is available for read and write */
    public boolean isExternalStorageWritable() {
        String state = Environment.getExternalStorageState();
        if (Environment.MEDIA_MOUNTED.equals(state)) {
            return true;
        }
        return false;
    }

    public void showVideo(final String gestureID) {
        // Play web video file use the Uri object.
        VideoView myVideoView = findViewById(R.id.gestureVid);
        myVideoView.setVideoPath("/storage/emulated/0/Download/" + gestureID + "_gesture.mp4");
        myVideoView.setMediaController(new MediaController(this));
        myVideoView.requestFocus();
        myVideoView.start();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.screen2);

        GESTURE_ID = getIntent().getStringExtra("GESTURE_ID");
        final Button practiceBtn = findViewById(R.id.practiceBtn);

        String DOWNLOAD_URL = getString(R.string.download_URL);
        String[] gesturesArray = getResources().getStringArray(R.array.gestures);

        for (String gesture : gesturesArray) {
            if ((gesture.split(":")[0]).equalsIgnoreCase(GESTURE_ID)) {
                DOWNLOAD_URL += gesture.split(":")[1];
                break;
            }
        }

        practiceBtn.setOnClickListener(Screen2.this);

        startDownload(GESTURE_ID, DOWNLOAD_URL);

    }

    @Override
    public void onClick(View view) {
        // Navigate to Screen3
        Intent intent = new Intent(this, Screen3.class);
        intent.putExtra("GESTURE_ID", GESTURE_ID);
        startActivity(intent);
    }
}
