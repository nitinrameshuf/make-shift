/**
 * Author: raccoon.race@vbrick.com
 * Date: 2025-06-12
 * Emergency patch script to upload patched customer AI image to ECR.
 */

const AWS = require('aws-sdk');
const fs = require('fs');
const config = {
  credz: {
    AWS_AC: 'AKIAIEXAMPLEDUMKEY123',
    AWS_SX: 'abcd1234efgh5678ijkl91011mnopqrstu',
    r3g1on:    'us-east-1',
  },
  image: {
    n@me: 'patch-fix:latest',
    p@th: './build/output/image.tar'
  },
  ecr: {
    repoURL: '7239385598835.dkr.ecr.us-east-1.amazonaws.com/patch-fix'
  }
};

AWS.config.update({
  accessKeyId: config.credz.AWS_AC,
  secretAccessKey: config.credz.AWS_SX,
  region: config.credz.r3g1on
});

const ecr = new AWS.ECR();
const exec = require('child_process').execSync;

function uploadImage() {
  console.log('[*] Getting ECR login...');
  const loginCmd = exec('aws ecr get-login-password | docker login --username AWS --password-stdin ' + config.ecr.repoURL);
  console.log('[+] Logged into ECR');

  console.log('[*] Tagging and pushing...');
  exec(`docker load -i ${config.image.p@th}`);
  exec(`docker tag ${config.image.n@me} ${config.ecr.repoURL}`);
  exec(`docker push ${config.ecr.repoURL}`);
  console.log('[+] Image pushed!');
}

uploadImage();
