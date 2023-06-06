<!-- markdownlint-disable -->

# API Overview

## Modules

- [`error`](./error.md#module-error)
- [`exec`](./exec.md#module-exec)
- [`genop`](./genop.md#module-genop)
- [`image`](./image.md#module-image)
- [`image_genop`](./image_genop.md#module-image_genop)
- [`minmax`](./minmax.md#module-minmax)
- [`noop`](./noop.md#module-noop)
- [`pynq_array_copy`](./pynq_array_copy.md#module-pynq_array_copy)
- [`pynq_parallel`](./pynq_parallel.md#module-pynq_parallel)
- [`pynq_vector_add`](./pynq_vector_add.md#module-pynq_vector_add)
- [`resource`](./resource.md#module-resource)
- [`session`](./session.md#module-session)
- [`sgemm`](./sgemm.md#module-sgemm)
- [`shared_object`](./shared_object.md#module-shared_object)
- [`tensorflow`](./tensorflow.md#module-tensorflow)
- [`test`](./test.md#module-test)

## Classes

- [`error.VaccelError`](./error.md#class-vaccelerror): Exception raised when a vAccel runtime error occurs
- [`exec.Exec`](./exec.md#class-exec): An Exec operation model vAccel resource
- [`exec.Exec_Operation`](./exec.md#class-exec_operation): An Exec Operation model vAccel resource
- [`exec.Exec_with_resource`](./exec.md#class-exec_with_resource): An Exec with resource model vAccel resource.
- [`exec.Vaccel_Args`](./exec.md#class-vaccel_args): A helper class for converting argument lists to the appropriate vAccel format
- [`genop.Genop`](./genop.md#class-genop)
- [`genop.VaccelArg`](./genop.md#class-vaccelarg)
- [`genop.VaccelArgInfo`](./genop.md#class-vaccelarginfo)
- [`genop.VaccelArgList`](./genop.md#class-vaccelarglist)
- [`genop.VaccelOpType`](./genop.md#class-vacceloptype): An enumeration.
- [`image.ImageClassify`](./image.md#class-imageclassify): An Image Classify model vAccel resource.
- [`image.ImageDepth`](./image.md#class-imagedepth): An Image Depth model vAccel resource
- [`image.ImageDetect`](./image.md#class-imagedetect): An Image Detect model vAccel resource
- [`image.ImagePose`](./image.md#class-imagepose): An Image Pose model vAccel resource
- [`image.ImageSegment`](./image.md#class-imagesegment): An Image Segment model vAccel resource
- [`image_genop.ImageClassify`](./image_genop.md#class-imageclassify)
- [`image_genop.ImageDepth`](./image_genop.md#class-imagedepth)
- [`image_genop.ImageDetect`](./image_genop.md#class-imagedetect)
- [`image_genop.ImagePose`](./image_genop.md#class-imagepose)
- [`image_genop.ImageSegment`](./image_genop.md#class-imagesegment)
- [`minmax.MinMax`](./minmax.md#class-minmax): A MinMax model vAccel resource.
- [`noop.Noop`](./noop.md#class-noop)
- [`pynq_array_copy.Pynq_array_copy`](./pynq_array_copy.md#class-pynq_array_copy): A Pynq array copy model vAccel resource.
- [`pynq_parallel.Pynq_parallel`](./pynq_parallel.md#class-pynq_parallel): A Pynq parallel model vAccel resource.
- [`pynq_vector_add.Pynq_vector_add`](./pynq_vector_add.md#class-pynq_vector_add): A Pynq vector add model vAccel resource.
- [`resource.Resource`](./resource.md#class-resource): A vAccel resource
- [`session.Session`](./session.md#class-session)
- [`sgemm.Sgemm`](./sgemm.md#class-sgemm): An Sgemm model vAccel resource.
- [`shared_object.Object`](./shared_object.md#class-object)
- [`tensorflow.Node`](./tensorflow.md#class-node): A representation of TensorFlow graph input or output node
- [`tensorflow.Tensor`](./tensorflow.md#class-tensor): A representation of a Tensor
- [`tensorflow.TensorFlowModel`](./tensorflow.md#class-tensorflowmodel): A TensorFlow model vAccel resource
- [`tensorflow.TensorType`](./tensorflow.md#class-tensortype): An enumeration.

## Functions

- [`test.test_exec_genop`](./test.md#function-test_exec_genop)
- [`test.test_exec_with_resource`](./test.md#function-test_exec_with_resource)
- [`test.test_genop`](./test.md#function-test_genop): should work, but it doesn't because the sanity check on vAccel
- [`test.test_image_class_genop`](./test.md#function-test_image_class_genop)
- [`test.test_image_classify`](./test.md#function-test_image_classify)
- [`test.test_image_depth`](./test.md#function-test_image_depth)
- [`test.test_image_depth_genop`](./test.md#function-test_image_depth_genop)
- [`test.test_image_detect`](./test.md#function-test_image_detect)
- [`test.test_image_detect_genop`](./test.md#function-test_image_detect_genop)
- [`test.test_image_pose`](./test.md#function-test_image_pose)
- [`test.test_image_pose_genop`](./test.md#function-test_image_pose_genop)
- [`test.test_image_segme_genop`](./test.md#function-test_image_segme_genop)
- [`test.test_image_segment`](./test.md#function-test_image_segment)
- [`test.test_min_max_genop`](./test.md#function-test_min_max_genop)
- [`test.test_noop`](./test.md#function-test_noop)
- [`test.test_pynq_array_copy_genop`](./test.md#function-test_pynq_array_copy_genop)
- [`test.test_pynq_parallel_genop`](./test.md#function-test_pynq_parallel_genop)
- [`test.test_pynq_vector_add_genop`](./test.md#function-test_pynq_vector_add_genop)
- [`test.test_session`](./test.md#function-test_session)
- [`test.test_sgemm_genop`](./test.md#function-test_sgemm_genop)


---


