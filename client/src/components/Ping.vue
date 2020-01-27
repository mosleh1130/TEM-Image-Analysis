<template>
  <div>
    <div class="row">
      <div class="row">
        <div class="col s6">
          <div class="file-field input-field">
            Choose an Image
            <div class="btn">
              <span>File</span>
              <input type="file" @change="onFileChange">
            </div>
            <div class="file-path-wrapper">
              <input class="file-path validate" type="text">
            </div>
          </div>
        </div>
        <div class="col s6">
          <div class="input-field">
            Filter Size: <b>{{ filter_size }}</b>
            <p class="range-field">
              <input type="range" v-model="filter_size" min="3" max="51" step="2">
            </p>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col s6">
          <div class="input-field">
            Sigma Color (SD of color space): <b>{{ sigma_color }}</b>
            <p class="range-field">
              <input type="range" v-model="sigma_color" min="5" max="150" step="1">
            </p>
          </div>
        </div>
        <div class="col s6">
          <div class="input-field">
            Sigma Space (SD of Co-ordinate space): <b>{{ sigma_space }}</b>
            <p class="range-field">
              <input type="range" v-model="sigma_space" min="5" max="150" step="1">
            </p>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col s6">
          Minimum Threshold: <b>{{ min_value }}</b>
          <p class="range-field">
            <input type="range" v-model="min_value" min="0" max="1" step="0.01">
          </p>
        </div>
        <div class="col s6">
          Maximum Threshold: <b>{{ max_value }}</b>
          <p class="range-field">
            <input type="range" v-model="max_value" min="0" max="1" step="0.01">
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col s4">
          Input Image
          <div id="preview">
            <img v-if="url" :src=input_url />
          </div>
        </div>
        <div class="col s4">
          Processed Image
          <div id="preview">
            <img v-if="grayscale_url" :src=grayscale_url />
          </div>
        </div>
        <div class="col s4">
          Output Image
          <div id="preview">
            <img v-if="output_url" :src=output_url />
          </div>
        </div>
      </div>
      <div class="row">
        <button class="btn waves-effect waves-light" type="submit" v-on:click="sendImage">Submit
          <i class="material-icons right">send</i>
        </button>
      </div>
      <div class="row">
        Particle Location and Size
        <div class="col s12">
          <table class="centered">
            <thead>
              <tr>
                <th>
                  Particle
                </th>
                <th>
                  Location (Co-ordinates)
                </th>
                <th>
                  Size (nm)
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in area" v-bind:key="item.id">
                <td>
                  {{ index+1 }}
                </td>
                <td>
                  {{ item.location }}
                </td>
                <td>
                  {{ item.size }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: '',
      url: null,
      file: {},
      area: [],
      input_url: [],
      grayscale_url: [],
      output_url: [],
      filter_size: 7,
      sigma_color: 50,
      sigma_space: 50,
      min_value: 0.13,
      max_value: 0.27,
    };
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files[0];
      this.file = file;
      this.url = URL.createObjectURL(file);
    },
    sendImage() {
      const path = 'http://localhost:5000/ping';
      const data = new FormData();
      data.append('image', this.file);
      data.append('filter_size', this.filter_size);
      data.append('sigma_color', this.sigma_color);
      data.append('sigma_space', this.sigma_space);
      data.append('min_value', this.min_value);
      data.append('max_value', this.max_value);
      const config = {
        header: {
          'Content-Type': 'multipart/form-data',
        },
      };
      axios.post(path, data, config)
        .then((res) => {
          this.msg = res.data;
          this.area = this.msg.area;
          [this.grayscale_url] = res.data.gray;
          [this.input_url] = res.data.input;
          [this.output_url] = res.data.output;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
  },
};
</script>
