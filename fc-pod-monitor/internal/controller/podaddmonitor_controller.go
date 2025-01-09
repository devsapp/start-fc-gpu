/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"fmt"
	"time"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/event"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/predicate"
)

// PodAddMonitorReconciler reconciles a PodAddMonitor object
type PodAddMonitorReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=fc-gpu.gpu.fc.serverless.aliyun,resources=podaddmonitors,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=fc-gpu.gpu.fc.serverless.aliyun,resources=podaddmonitors/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=fc-gpu.gpu.fc.serverless.aliyun,resources=podaddmonitors/finalizers,verbs=update
// +kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch
// +kubebuilder:rbac:groups=core,resources=events,verbs=get;list;watch

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// TODO(user): Modify the Reconcile function to compare the state specified by
// the PodAddMonitor object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.19.1/pkg/reconcile
func (r *PodAddMonitorReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	_ = log.FromContext(ctx)

	// TODO(user): your logic here
	_, fcHookUrl, fcHookHost, podPort, err := GetEnvs()
	if err != nil {
		return ctrl.Result{}, err
	}

	var pod corev1.Pod

	podIP := ""
	maxRetries := 600
	for attempt := 1; attempt <= maxRetries; attempt++ {
		fmt.Printf("attempt: %d to try to get the ip of pod that was created.\n", attempt)
		if err := r.Get(ctx, req.NamespacedName, &pod); err != nil {
			fmt.Printf("unable to fetch Pod for err: %v", err)
			return ctrl.Result{}, client.IgnoreNotFound(err)
		}

		podIP = pod.Status.PodIP
		if podIP != "" {
			break
		}
		time.Sleep(6 * time.Second)
	}
	podIP = fmt.Sprintf("%s:%d", podIP, podPort)
	fmt.Printf("One Pod with IP: %s was created.\n", podIP)

	// 通知FC
	PodUpdateCallback(fcHookUrl, fcHookHost, podIP, "Add")

	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *PodAddMonitorReconciler) SetupWithManager(mgr ctrl.Manager) error {
	watchNamespace, fcHookUrl, fcHookHost, podPort, err := GetEnvs()
	if err != nil {
		fmt.Printf("Error occurs: %v, exit SetupWithManager.\n", err)
		return err
	}

	fmt.Printf("PodAddMonitorReconciler WATCH_NAMESPACE: %s, FC_HOOK_URL: %s, FC_HOOK_HOST: %s, POD_PORT: %d\n", watchNamespace, fcHookUrl, fcHookHost, podPort)

	startTime := time.Now()
	pred := predicate.Funcs{
		CreateFunc: func(e event.CreateEvent) bool {
			return e.Object.GetCreationTimestamp().After(startTime) && e.Object.GetNamespace() == watchNamespace
		},
		DeleteFunc: func(e event.DeleteEvent) bool {
			return false
		},
		UpdateFunc: func(e event.UpdateEvent) bool {
			return false
		},
		GenericFunc: func(e event.GenericEvent) bool {
			return false
		},
	}

	return ctrl.NewControllerManagedBy(mgr).
		// Uncomment the following line adding a pointer to an instance of the controlled resource as an argument
		For(&corev1.Pod{}).
		WithEventFilter(pred).
		Named("PodAddMonitor").
		Complete(r)
}
