{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 9,
      "minor": 0,
      "revision": 4,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      59.0,
      119.0,
      1000.0,
      677.0
    ],
    "gridsize": [
      15.0,
      15.0
    ],
    "boxes": [
      {
        "box": {
          "id": "obj-6",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            269.0,
            296.0,
            34.0,
            22.0
          ],
          "text": "*~ 1."
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "bang"
          ],
          "patching_rect": [
            450.0,
            242.0,
            34.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "maxclass": "flonum",
          "patching_rect": [
            300.0,
            300.0,
            50.0,
            22.0
          ],
          "id": "obj-14",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "bang"
          ]
        }
      },
      {
        "box": {
          "addpoints": [
            0.0,
            0.0,
            0,
            63.829787234042556,
            0.2,
            0,
            122.34042553191489,
            0.64,
            0,
            329.78723404255317,
            0.213333333333333,
            0,
            1000.0,
            0.0,
            0
          ],
          "classic_curve": 1,
          "id": "obj-10",
          "maxclass": "function",
          "numinlets": 1,
          "numoutlets": 4,
          "outlettype": [
            "float",
            "",
            "",
            "bang"
          ],
          "parameter_enable": 0,
          "patching_rect": [
            450.0,
            111.0,
            200.0,
            100.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "spectroscope~",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            393.0,
            395.0,
            300.0,
            100.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "gain~",
          "multichannelvariant": 0,
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            ""
          ],
          "parameter_enable": 0,
          "patching_rect": [
            267.0,
            332.0,
            158.0,
            24.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-3",
          "maxclass": "button",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "bang"
          ],
          "parameter_enable": 0,
          "patching_rect": [
            267.0,
            111.0,
            37.0,
            37.0
          ]
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "ezdac~",
          "numinlets": 2,
          "numoutlets": 0,
          "patching_rect": [
            267.0,
            395.0,
            45.0,
            45.0
          ]
        }
      },
      {
        "box": {
          "maxclass": "kslider",
          "patching_rect": [
            59.0,
            119.0,
            336.0,
            66.0
          ],
          "id": "obj-12",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "int",
            "float"
          ]
        }
      },
      {
        "box": {
          "maxclass": "newobj",
          "text": "mtof",
          "patching_rect": [
            59.0,
            190.0,
            38.0,
            22.0
          ],
          "id": "obj-13",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "float"
          ]
        }
      },
      {
        "box": {
          "id": "obj-1",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            267.0,
            258.0,
            66.0,
            22.0
          ],
          "text": "cycle~ 440"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-6",
            0
          ],
          "source": [
            "obj-1",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-11",
            0
          ],
          "source": [
            "obj-10",
            1
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-6",
            1
          ],
          "source": [
            "obj-11",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-2",
            1
          ],
          "order": 1,
          "source": [
            "obj-4",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-2",
            0
          ],
          "order": 2,
          "source": [
            "obj-4",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-9",
            0
          ],
          "order": 0,
          "source": [
            "obj-4",
            0
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-6",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-11",
            0
          ],
          "destination": [
            "obj-14",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-3",
            0
          ],
          "destination": [
            "obj-10",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-12",
            0
          ],
          "destination": [
            "obj-13",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-13",
            0
          ],
          "destination": [
            "obj-1",
            0
          ]
        }
      }
    ],
    "originid": "pat-37",
    "dependency_cache": [],
    "autosave": 0
  }
}