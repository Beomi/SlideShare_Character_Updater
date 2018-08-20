<template>
    <div class="container">
        <!-- Styled -->
        <hr>
        <div v-show="!isOneUploadComplete && !isProcessFinished" id="uploader">
            <Gallery :uploader="uploader"/>
        </div>
        <loading-circle v-show="isOneUploadComplete && !isProcessFinished" id="loadingcircle"></loading-circle>
        <div v-show="isProcessFinished">
            <h2>Converting Finished!</h2>
            <h4>
                <small>refresh page to try another files</small>
            </h4>
            <a :href="pdfUrl">
                <b-button>Download PDF</b-button>
            </a>
        </div>
    </div>
</template>

<script>
    import Gallery from 'vue-fineuploader/gallery'
    import FineUploaderS3 from 'fine-uploader-wrappers/s3'
    import LoadingCircle from "@/components/LoadingCircle";

    const sleep = (ms) => {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    export default {
        components: {
            LoadingCircle,
            Gallery
        },
        data() {
            const randomKey = Math.random().toString(36).substring(7);
            const now = new Date()

            let isOneUploadComplete = false
            let isProcessFinished = false

            const onComplete = async (id, originalFileName, object, xhr) => {
                this.isOneUploadComplete = true
                while (true) {
                    const fileName = `${randomKey}_${originalFileName.replace('.pdf', '').replace(/\W/gi, "_")}.pdf`
                    const s3Key = `${now.toISOString().split('T')[0]}/${fileName}`
                    try {
                        const total_url = 'https://s3.ap-northeast-2.amazonaws.com/slidesharecharacteruploader/downloads/'
                            + encodeURIComponent(s3Key).replace('%2F', '/')
                        const res = await this.axios.get(total_url)
                        if (res.status === 200) {
                            this.isProcessFinished = true
                            this.pdfUrl = total_url
                            return;
                        }
                    } catch (e) {
                        await sleep(2000)
                    }
                }
            }

            const onValidate = (fileOrBlobData) => {
                const fileName = fileOrBlobData.name
                return !!fileName.endsWith('.pdf');
            }

            const uploader = new FineUploaderS3({
                options: {
                    request: {
                        endpoint: 'https://slidesharecharacteruploader.s3.amazonaws.com',
                        accessKey: 'AKIAIEBKNKEW6V3UPN4Q'
                    },
                    signature: {
                        version: 4,
                        endpoint: 'https://52o6ty6nsc.execute-api.ap-northeast-2.amazonaws.com/api/'
                    },
                    objectProperties: {
                        region: 'ap-northeast-2',
                        key(fileId) {
                            const originalFileName = this.getName(fileId)
                            const fileName = `${randomKey}_${originalFileName.replace('.pdf', '').replace(/\W/gi, "_")}.pdf`
                            const s3Key = `uploads/${now.toISOString().split('T')[0]}/${fileName}`
                            return s3Key
                        }
                    },
                    callbacks: {
                        onComplete,
                        onValidate
                    }
                },
            })
            return {
                uploader,
                isOneUploadComplete,
                isProcessFinished,
                pdfUrl: '',
            }
        }
    }
    //
    // export default {
    //     data() {
    //         return {
    //             s3Key: '',
    //             s3Url: 'https://slidesharecharacteruploader.s3.amazonaws.com'
    //         }
    //     },
    //     methods: {
    //         async submit(e) {
    //             e.preventDefault()
    //             const now = new Date()
    //             const form = e.target
    //             const firstFile = form.file.files[0]
    //             if (!this.validateIsPdf(firstFile)) {
    //                 return false
    //             }
    //             this.s3Key = `uploads/${now.toISOString()}/${this.fileName}`
    //             const formData = new FormData(form)
    //             const res = await this.axios.post(this.s3Url, formData)
    //             console.log(res)
    //         },
    //         validateIsPdf(file) {
    //             return !!(file.name.endsWith('.pdf') && file.type === "application/pdf");
    //         }
    //     },
    // }
</script>
